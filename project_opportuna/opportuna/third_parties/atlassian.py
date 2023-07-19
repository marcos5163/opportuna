import requests
from opportuna.models import Post


class AtlassianIntegrationService:
    def __init__(self) -> None:
        return

    def get_atlassian_job_postings(self):

        url = "https://www.atlassian.com/.rest/postings" 
        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None
        
        print("response status", response.status_code)
        if response.status_code == 200:
            return response.json()

    def process_result(self, json_resp):
        
        processed_result = []
        for post in json_resp['postings']: 
            if post.get('requisition') and 'Engineer' in post.get('requisition').get('name'):
                processed_result.append(post)

        return processed_result  

    def extract_data_and_save(self, results: list):
        
        post_obj = []

        try:
            for result in results:
                title = result['requisition']['name']
                desc = ""
                for list in result['content']['lists']:
                    if list['text'] == "Your background":
                     desc = list['content']
                     break
                    else:
                        desc = ""


                apply_url = result['urls'].get('applyUrl') if result.get('urls') else ""
                location = result['requisition']['location']
                is_remote = True if 'Remote' in result['tags'] else False
                unique_atlassian_id = result['requisition']['id']

                post_obj.append(Post(title = title, discription = desc, company = 'atlassian', 
                                    meta_tags = {'location':location, 
                                    'apply_url':apply_url, 
                                    'is_remote': is_remote,
                                    'unique__third_party_id': unique_atlassian_id}))
                print(title)
        except Exception as error:
            print(str(error))        
            
        try:
            Post.objects.bulk_create(post_obj, batch_size=100)
        except Exception as e:
            print("error while creating", str(e))  

    def main(self):

        json_resp = self.get_atlassian_job_postings()

        filtered_results = self.process_result(json_resp=json_resp)

        self.extract_data_and_save(results=filtered_results)


            

                
           
    
              

              
        