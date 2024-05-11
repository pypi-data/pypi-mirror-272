from openai import AzureOpenAI, OpenAI
from bs4 import BeautifulSoup
import tqdm
import time
import pandas as pd
import json
import logging
import httpx
import validators
import importlib_resources

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Scrapper:
    def __init__(self, url):
        self.url = url

    def scrape_first_level_content(self):
        try:
            # Use httpx to fetch the contents of the website
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
            }
            response = httpx.get(self.url, headers=headers, follow_redirects=True, verify=False)
            response.raise_for_status()  # Will raise an exception for 4XX/5XX responses

            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find first-level content, e.g., direct children of the <body> tag or main content tags
            # This example assumes first-level content is within <p>, <h1>, and <h2> tags
            content_tags = soup.find_all(['h1', 'h2', 'p'])

            # Extracting the text from the selected tags
            contents = [tag.get_text(strip=True) for tag in content_tags]

            return contents

        except Exception as e:
            raise e


class CompanyQualificationTool:
    def __init__(self, client: AzureOpenAI | OpenAI, model: str, temperature=0, prompt_qualification_template_path=None,
                 browsing=False, browsing_key=None, prompt_find_website_template=None):

        my_templates = importlib_resources.files("qualif") / "templates"
        if prompt_qualification_template_path is None:
            self.prompt_find_website = (my_templates / "prompt_find_website_template.txt").read_text()
        else:
            self.prompt_qualification = open(prompt_qualification_template_path).read()
        if prompt_find_website_template is None:
            self.prompt_qualification = (my_templates / "prompt_qualification_template.txt").read_text()
        else:
            self.prompt_find_website = open(prompt_find_website_template).read()

        self.model = model
        self.client = client
        self.browsing = browsing
        self.browsing_key = browsing_key
        self.time_sleep = 0.1
        self.temperature = temperature

    def complete(self, messages) -> str | None:
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    n=1,
                )
                time.sleep(0.1)

                all_responses = [response.choices[i].message.content for i in range(len(response.choices))]
                return all_responses[0]

            except Exception as e:
                # if get limit error, wait for some time to run again
                if ("limit" in str(e)):
                    logger.warning(msg=e)
                    time.sleep(self.time_sleep)
                else:
                    logger.error(msg=f"Failed to invoke azure openai service. Error msg: {e}")
                    break
        return None

    def bing_search(self, query: str, top_k=10) -> json:
        """
        This function is used to find website address.
        https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/reference/query-parameters
        :param query:
        :param top_k: the number of records to keep.
        :return:
        """
        results = []
        web_search_endpoint = "https://api.bing.microsoft.com/v7.0/search"

        headers = {
            'Ocp-Apim-Subscription-Key': self.browsing_key
        }

        params = {
            'q': query,
            'count': top_k,
            'responseFilter': 'Webpages'
        }

        response = httpx.get(web_search_endpoint, headers=headers, params=params)
        for webpage in response.json()['webPages']['value']:
            webpage_entry = {}
            webpage_entry["url"] = webpage['displayUrl']
            webpage_entry["snippet"] = webpage['snippet']
            results.append(webpage_entry)
        return results

    def find_website(self, partner_name: str) -> str | None:
        if self.browsing:
            bing_search_results = self.bing_search(query=f"{partner_name} website address")
            cur_prompt = (self.prompt_find_website.replace('{{Entreprise}}', partner_name))
            cur_prompt = cur_prompt.replace('{{BING_RESULTATS}}', f"{bing_search_results}")
            messages = [
                {"role": "system", "content": "Tu es un expert dans la qualification des partenaires indirectes"},
                {"role": "user", "content": cur_prompt}
            ]
            website = self.complete(messages=messages)

        if validators.url(website):
            return website
        # loop at least
        return None

    def find_website_loop(self, partner_name: str, max_loop=3) -> str | None:
        """
        Try to find website for max_loop times, return website if found, otherwise return None.
        :param partner_name:
        :param max_loop:
        :return:
        """
        cur_loop = 1
        website = None
        while cur_loop <= max_loop:
            website = self.find_website(partner_name)
            if website is not None:
                break
            cur_loop += 1
        return website

    def qualify(self, partner_name: str) -> json:
        final_result = {}

        cur_prompt = self.prompt_qualification.replace('{{Entreprise}}', partner_name)
        messages = [
            {"role": "system", "content": "Tu es un expert dans la qualification des partenaires indirectes"},
            {"role": "user", "content": cur_prompt}
        ]

        if self.browsing:
            website = self.find_website_loop(partner_name)
            final_result["site_web"] = website
            web_content = None
            try:
                web_content = Scrapper(url=website).scrape_first_level_content()
            except Exception as e:
                final_result["site_web"] = "Information non disponible"

            if web_content:
                messages.append({
                    "role": "assistant",
                    "content": f"Vous avez aussi le contenu scrapé du siteweb que vous pouvez utiliser pour constituer la réponse de la qualification. {web_content}"
                })

        response = self.complete(messages=messages)
        if response is not None:
            json_response = json.loads(response.replace("```json", "").replace("```", ""))
            final_result.update(json_response)
            return final_result
        return response

    def batch(self, df_partners: pd.DataFrame, col_name_partner: str) -> pd.DataFrame:
        """
        :param df_partenaires: original panda dataframe that should contain at least a column of partner names
        :param col_name: the column name of the partner name
        :return: final_df: enriched panda dataframe that will contain site_web, secteurs, metier, Offres
        """
        # Initialize an empty DataFrame
        start_time = time.time()
        final_df = pd.DataFrame()
        for index, row in tqdm.tqdm(df_partners.iterrows()):
            partner = row[col_name_partner]
            json_response = self.qualify(partner_name=partner)
            if json_response is not None:
                logger.info(f"--- {time.time() - start_time} seconds --- {partner} ok")
                if self.browsing:
                    row["site_web"] = json_response["site_web"]
                row["secteurs"] = json_response["Secteur_d_Activite"]
                row["metier"] = json_response["Metier"]
                row["offres"] = json_response["Offres"]
                df_row = row.to_frame().T
                final_df = pd.concat([final_df, df_row], ignore_index=True)
        return final_df


if __name__ == '__main__':
    # Load Data
    df_partenaires = pd.read_excel("../partners_conseil_informatique_6202.xlsx")
    df_partenaires_sample = df_partenaires.sample(n=10, random_state=52)
    df_partenaires_sample

    azure_endpoint = "https://chatgpt-dp-innovation-dev.openai.azure.com/"
    apikey = "58d9c01f9ced46f480a5356bbb6d94da"
    browsing_key = 'fb37d55b3ffc4ed49015366c0f078907'
    apiversion = "2024-02-15-preview"
    model = "smb"

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=apikey,
        api_version=apiversion,
    )

    tool = CompanyQualificationTool(client=client, model=model, temperature=0, browsing=True, browsing_key=browsing_key)
    result = final_df = tool.qualify("APITECH")
    print(result)
