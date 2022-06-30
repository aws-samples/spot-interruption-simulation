import time
import concurrent.futures
import requests

__author__ = "ssengott@"
#availability scoring lambda. to be invoked asynchronously
def lambda_handler(event, context):
    print("availability check lambda.")
    print(event)
    app_url = event["app_url"]
    start_time_availability = time.time()

    print("processing for app_url" + app_url)
    #for app_url of the team, call competitive_scoring_util.avail_check() which will return availability score
    #50 parallel worker, total hit - 500 (50 at a time.. so, 10 times in parallel)
    error_rate_5xx = avail_check_score(app_url, 1400, 100)
    end_time = time.time()
    print(f"Runtime of availability check is: {end_time - start_time_availability}")


def open_url(url)->dict:
    result_dict = {'status_code': 503}
    start = time.time()
    try:
        res = requests.get(url)
        end = time.time() - start
        # print(res.status_code)
        result_dict['status_code'] = res.status_code
        result_dict['time_taken'] = end
    except Exception as excp:
        end = time.time() - start
        #print(res.status_code)
        # setting bad response
        result_dict['status_code'] = 400
        result_dict['time_taken'] = end
        print("GD: Exception:" + str(excp))

    return result_dict

#temporary method to append url num_of_times
def prepare_url_list(app_url, num_of_times):
    urls = []
    for n in range(num_of_times):
        urls.append(app_url)
    return urls

def avail_check_score(app_url, num_of_times, worker_count):
    #hit app_url for mentioned number of times split with parallel worker_count
    urls = prepare_url_list(app_url,num_of_times)
    status_5xx_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        res_dict = executor.map(open_url, urls)
        print("execution------------------------------------")
        for entry in res_dict:
            print("-", end=" ")
            #print("entry=" + str(ent))
            status_code = entry['status_code']
            #print("status-code=" + str(status_code))
            if status_code >= 500 and status_code <= 599 :
                status_5xx_count = status_5xx_count + 1
                print("     5xx error.......................")
            if entry['status_code'] !=200 :
                print("     non 200 status ******************************-------------"+ str(status_code))

    #calculate % of non 5xx errors, so that score can be calculated
    error_rate = (status_5xx_count / num_of_times)
    print("app url 5xx percentage=" + str(error_rate))
    print("app url 5xx percentage=" + str(status_5xx_count))
    availability_score =0
    #calculate availability score
    if error_rate == 0:
        print("all 200 response")
    return error_rate
