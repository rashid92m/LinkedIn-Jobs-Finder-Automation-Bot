from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
from selenium.webdriver.support.ui import Select
import time
import json
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

#Update Your email id and password Here
USERNAME = "abc@gmail.com" #add you linkedin gmail ID here
PASSWORD = "******" #add you linkedin password here
all_url_list = []
job_search_keyword_info= input('job_search_keyword_info ')
url = input('Insert Job URl of Job Listing page: ')
if url is "":
    print(f"read url from url.txt file")
    with open('urls.txt', 'r') as url_input_file:
        all_url_list = url_input_file.readlines()
    print(f"Total urls : {len(all_url_list)}")
else:
    all_url_list.append( url)

# AUtomation test engineer, UK
# url = "https://www.linkedin.com/jobs/search/?currentJobId=3336108443&distance=25&f_JT=F&geoId=101165590&keywords=automation%20test%20engineer"
# url =[]
# url.append("https://www.linkedin.com/jobs/search/?currentJobId=3426899152&f_C=86811903&geoId=92000000&originToLandingJobPostings=3426899152%2C3424066953%2C3397921683%2C3424062416%2C3387419528%2C3376792827%2C3381704487%2C3387291446%2C3368700508")

# MaxApply = int(input('MaxApplyCount'))

applyNowButtonArial = ""
company, job_title, location, workplace_type, job_title_href_element, job_type, employees_count_and_type, job_postion_href, employees_count, company_type  = ["NA"] * 10
ignored_exceptions = (StaleElementReferenceException,)
path = r'C:\Users\Rashid mohammad\Downloads\edgedriver_win64\msedgedriver.exe'
driver = webdriver.Edge(path)
driver.implicitly_wait(5) # seconds



wait = WebDriverWait(driver, 5)

xpath_rememberME = '/html/body/div/main/div/section/header/h3[2]'
xpath_cancel_remember_me = '/html/body/div/main/div/section/footer/form[1]/button'
xpath_job_description = "//div[contains(@id, 'job-detail')]"
list_of_must_have_keyword_description = ["python"]
list_of_must_skip_keyword_description = ["good knowledge of German"]
skip_job_keyword_title =['Developer','German Speaking', 'programmer','main frame', 'Mainframe', 'manager','java', 'javascript', 'Devops', 'Full stack', 'Fullstack', 'salesforce' ]

must_have_keyword_title =['Quality', 'Assurance', 'QA', 'SDET', 'Automation','Test', 'Analyst', 'Manual', 'Tester',
                          'Validation', 'Automation', 'testing', 'bdd' ]


job_type = "NA"
employees_count_and_type = "NA"
ONLY_COLLECT_JOB_URL = True

def minimize_chat_window():

    xpathof_button = '//*[@id="msg-overlay"]/div[1]/header/section[1]/button'
    try:
        print('minimizing chat window...')
        down_button= wait.until(EC.visibility_of_element_located((By.XPATH, xpathof_button)))
        down_button.click()
    except TimeoutException:
        print("ERROR: Chat window is not minimized ")

def sign_out():
    dropdown_button = driver.find_element_by_css_selector('.artdeco-dropdown__trigger--placement-bottom')
    dropdown_button.click()
    signout_button = driver.find_element_by_xpath('//*[@href="/m/logout/"]')
    signout_button.click()


def sign_in():
    my_dynamic_element = driver.find_element_by_class_name("cta-modal__primary-btn")
    my_dynamic_element.click()
    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    sign_in_button = driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/form/div[3]/button")
    sign_in_button.click()

    #Check For remeber ME window and click cancel
    try:
        remember_me= wait.until(EC.presence_of_element_located((By.XPATH, xpath_rememberME)))
        if remember_me.text == 'Remember me on this browser':
            driver.find_element_by_xpath(xpath_cancel_remember_me).click()

    except TimeoutException:
        print("ERROR: Remember ME box not avaible,Continue... ")

def discard():
    try:
        cancel_button = driver.find_element_by_css_selector("button.artdeco-modal__dismiss")
        if cancel_button.is_enabled():
            time.sleep(1)
            cancel_button.click()
            time.sleep(1)
            discard_button = driver.find_element_by_css_selector("button.artdeco-modal__confirm-dialog-btn.artdeco-button--secondary")
            if discard_button.is_enabled():
                time.sleep(1)
                discard_button.click()

                time.sleep(1)
                print(f"Application for {company} is discarded")
                return True
            else:
                print("Discard button is not enabled")
                return False
        else:
            print("Cancel button is not enabled")
            return False
    except NoSuchElementException:
        print("ERROR : Unable to click Cancel or Discard button")
        return False


def click_review():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click review button")
        assert discard(), "Discard Fail"
        return False

def clickSubmit():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click Submit button")
        assert discard(), "Discard Fail"
        return False

def clickNext():
    try:
        driver.find_element_by_css_selector(
            "footer > div > button.artdeco-button--primary").click()  # review Button
        return True
    except NoSuchElementException:
        print("ERROR : Unable to click Next button")
        assert discard(), "Discard Fail"
        return False


def checkSubmitSuccessfull():
    return_flag = False
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.jpac-modal-header")))
        submitHeading= driver.find_element_by_css_selector("h3.jpac-modal-header")
        submitText = submitHeading.text
        if "Your application was sent to" in submitText:
            print(f"{submitText} ")
            return_flag = True
        else:
            print(f"{submitText} ")
    except NoSuchElementException:
        print(f"Application submission fails for {applyNowButtonArial} ")
    finally:
        driver.find_element_by_css_selector("button.artdeco-modal__dismiss").click()

    return return_flag

def job_information_from_card(job_list_element):
    global job_title_href, job_title_href_element, job_title, company, location, workplace_type, job_title_href_element
    try:
        job_title = job_list_element.find_element_by_xpath(".//a[contains(@class, 'job-card-container__link job-card-list__title')]").get_attribute('innerText')
        job_title_href_element = job_list_element.find_element_by_xpath(".//a[contains(@class, 'job-card-container__link job-card-list__title')]")
        job_title_href = job_title_href_element.get_attribute("href")

        company = job_list_element.find_element_by_xpath(".//a[contains(@class, 'job-card-container__link job-card-container__company-name')]").get_attribute('innerText')
        location = job_list_element.find_element_by_xpath(".//li[contains(@class, 'job-card-container__metadata-item')][1]").get_attribute('innerText')
        workplace_type = job_list_element.find_element_by_xpath(".//li[contains(@class, 'job-card-container__metadata-item job-card-container__metadata-item--workplace-type')]").get_attribute('innerText')
        print(f"Job card info: {job_title}---{company}---{location}---{workplace_type}")
        return True
    except BaseException:
        print(f"Error: unable to collect job information from card")
        return False


def send_msg_to_recruiter():
    try:
        msg_to_recruiter_button = driver.find_element_by_xpath("//div[contains(@class , 'hirer-card__message-container')]/*/a")
        href_of_msg_button = msg_to_recruiter_button.get_attribute("href")
        if href_of_msg_button.startswith("https://www.linkedin.com/premium"):
            #skip messaging Premium subscription is required
            pass
        elif href_of_msg_button.startswith("/messaging/thread"):
            msg_to_recruiter_button.click()
            upload_resume_input = driver.find_element_by_xpath("//div[contains(@class,'msg-form__upload-attachment inline-bloc')][2]/input[contains(@type,'file')]")
            upload_resume_input.send_keys("Resume_Rashid_AutomationTestEngineer.pdf")
            send_button = driver.find_element_by_xpath("//button[contains(@type,'submit')]")
            send_button.click()
        else:
            print("ERROR: recruiter massage link is not matched")
    except BaseException:
        print("ERROR: Unable to send msg to recruiter")


def remove_notification():
    # dismiss if any notification is showing
    # NOTE: notification is only shows when job is saved
    try:
        notification_dismiss_button = driver.find_elements_by_xpath(
            "*//button[contains(@class,'artdeco-toast-item__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view')]")
        if len(notification_dismiss_button) != 0:
            for each_notification in range(0, len(notification_dismiss_button)):
                notification_dismiss_button[each_notification].click()
                time.sleep(1)
    except BaseException:
        print("ERROR: Issue in notification handling")


def findAllJobsList():
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label,'Page ')]")))
    paginator_elements = driver.find_elements_by_xpath("//button[contains(@aria-label,'Page ')]")
    # last element of paginator shows last page as property 'aria-label'= "Page 40"
    last_page_no = paginator_elements[-1].get_attribute("aria-label")
    last_page_no_int = int(last_page_no[5:])
    page_count = 1
    job_count = 1
    for page_count in range(1, last_page_no_int+1):

        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.jobs-search-results__list-item")))

        allJobs = driver.find_elements_by_css_selector("li.jobs-search-results__list-item")
        print(f"page {page_count} : Total Jobs listed are {len(allJobs)}")
        start_time = 0
        for job in allJobs :

            print(f"\ntime taken to operate above job : {time.time() - start_time} sec")
            start_time = time.time()
            remove_notification()


            try:
                ActionChains(driver).move_to_element(job).perform()
                job_title_div = WebDriverWait(job, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[@data-job-id]")))

                time.sleep(1)
                job_title_div.click()
                job_information_from_card(job)

                print(f"job_title_href is : {job_title_href}")
                # check if this job Url is already checked in previous execution and skip if yes
                job_id = job_title_href.split('/')[5]
                if job_id in already_checked_jobs_str:
                    print("INFO : This job ID is already checked previously, skip this job.. ")
                    continue

                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[contains(@aria-label, '{job_title}')]")))
                except TimeoutException:
                    print("ERROR: job detail container is not loaded ")
                    current_url = str(driver.current_url)
                    if current_url.startswith('https://www.linkedin.com/company/'):
                        print(f"ERROR: company page opened: url : {current_url} ")
                        driver.back()
                        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.jobs-search-results__list-item")))
                        continue
            except BaseException:
                print("ERROR: Element is not clickable")
                continue

            print(f"\nstarting apply process for {company}")
            apply_decision_flag = apply_decision()
            print(f"apply decision is {apply_decision_flag}")
            if apply_decision_flag:
                if ONLY_COLLECT_JOB_URL:
                    filtered_job_details = f"\n{job_postion_href}   {company}   {job_title}   {location}    {workplace_type}    {job_type}   {employees_count}   {company_type}"
                    try:

                        with open("filtered_job.txt", 'a') as filtered_job:
                            filtered_job.write(filtered_job_details)
                        save_job_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-save-button")))
                        save_job_button_text = save_job_button.get_attribute('innerText')
                        #if job is already saved skip it.
                        if "Saved" in save_job_button_text:
                            pass
                        elif "Save" in save_job_button_text:
                            ActionChains(driver).move_to_element(save_job_button).click().perform()

                        #after job is saved or applied, add Job id to alrady_checked_jobs.txt file
                        saved_job_id = f"\n{job_title_href}"
                        with open("already_checked_jobs.txt", 'a') as already_checked_jobs:
                            already_checked_jobs.write(saved_job_id)
                        time.sleep(1)
                        # print(filtered_job_details)
                    except BaseException:
                        print("ERROR: job is not saved")

                    continue

                try:
                    send_msg_to_recruiter()
                    applyNowButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-button")))
                    if applyNowButton.is_enabled():
                        global applyNowButtonArial
                        applyNowButtonArial = applyNowButton.get_attribute('aria-label')
                        print(f"applying for {applyNowButtonArial}")
                        time.sleep(1)
                        applyNowButton.click()
                        time.sleep(2)
                        # Note: Contact Info Screen, details are prefilled
                        #check heading on form screen and do operation accordingly

                        try:

                            firstbutton = driver.find_element_by_css_selector('form footer button.artdeco-button--primary')
                            aria_label = firstbutton.get_attribute("aria-label")
                            # fill the form untill Review page is displayed or max try reaches
                            form_page_max_retry = 8
                            form_counter = 0
                            while "Review your application" not in aria_label  and form_counter < form_page_max_retry:
                                form_heading_h3 = driver.find_element_by_xpath(
                                    "//form//h3[contains(@class,'t-16')]").get_property('innerText')
                                if "Contact info" in form_heading_h3 :
                                    pass
                                elif "Home address" in form_heading_h3 :
                                    fill_additional_question(homeAddress=True)
                                elif "Resume" in form_heading_h3:
                                    pass
                                elif form_heading_h3 in ["Additional Questions", "Additional", "Work authorization" ]:
                                    fill_additional_question()
                                elif "Work experience" in form_heading_h3:
                                    pass
                                elif "Education" in form_heading_h3:
                                    pass
                                elif "Photo" in form_heading_h3:
                                    pass
                                    print("Photo_required_in this form")
                                else:
                                    print(f"{form_heading_h3} details required in form,heading does not matched")
                                    discard()
                                    break

                                time.sleep(2)

                                firstbutton = driver.find_element_by_css_selector(
                                    'form footer button.artdeco-button--primary')
                                aria_label = firstbutton.get_attribute("aria-label")
                                clickNext()
                                form_counter += 1

                            if "Review your application" in aria_label:
                                clickSubmit()
                                if checkSubmitSuccessfull():
                                    applied_job_details = f"\n{company}---{job_title}---{location}---{workplace_type}---{job_type}---{employees_count}---{company_type}"
                                    with open("applied_job_details.txt", 'a') as job_detail_file:
                                        job_detail_file.write(applied_job_details)
                            else:
                                discard()
                        except BaseException:
                            line_to_add_in_txt_file = "ERROR: Form heading is not found"
                            print("ERROR: Form heading is not found")
                            #discard and continue to new job
                            discard()


                    else:
                        print(f"Apply Now button is not available for {company}")
                except (NoSuchElementException,TimeoutException):
                    print(f"Error: JOb application failed for {company}")
            else:
                print(f"Error: Apply decision is false")
                # if applydision is taken for this jon, add Job id to already_checked_jobs.txt file
                job_already_procesed = f"\n{job_title_href}"
                with open("already_checked_jobs.txt", 'a') as already_checked_jobs:
                    already_checked_jobs.write(job_already_procesed)


            # After all jobs of Page 1 is completed, open 2nd page

        if page_count < last_page_no_int:
            try:
                print(f"INFO :load next page url")
                next_page_url = f"{url}&start={25 * page_count}"

                driver.get(next_page_url)
                time.sleep(5)
            except TimeoutException:
                print(f"INFO : Paginator search button *//button[contains(@aria-label,'Page {page_count + 1}')]")
                next_page_element = driver.find_element_by_xpath(
                    f"*//button[contains(@aria-label,'Page {page_count + 1}')]")
                ActionChains(driver).move_to_element(next_page_element).click().perform()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    f"*//button[contains(@aria-label,'Page {page_count + 1}') and contains(@aria-current,'true')]")))
            page_count+=1



def apply_decision():
    try:
        global job_postion_href, employees_count, company_type, job_title
        job_postion_href = driver.find_element_by_xpath("//div[@class='jobs-unified-top-card__content--two-pane']/a").get_attribute("href")
        jon_discription_article = driver.find_element_by_xpath("//*[contains(@class , 'jobs-description__container')]")
        jon_discription_text = str(jon_discription_article.get_attribute("innerText")).lower()
        job_details_list = driver.find_elements_by_xpath("//*[contains(@class , 'jobs-unified-top-card__content--two-pane')]/*//li")
        job_type = job_details_list[0].get_attribute('innerText')

        #NOTE: split character in linkedIn is NOT exactly DOT char('.'), it is ('·') differece in vertical allignment
        #Example:    "51-200 employees · Software Development"  or "10,001+ employees · Financial Services"
        employees_count_and_type = job_details_list[1].get_attribute('innerText')
        employees_count_and_type_list = str(job_details_list[1].get_attribute('innerText')).split("·")

        employees_count = employees_count_and_type_list[0]
        min_employees_count =  int((employees_count.split("-")[0] if "-" in employees_count else employees_count.split("+")[0]).replace(",",""))

        flag = False
        for each_keyword in must_have_keyword_title:
            if each_keyword.lower() in job_title.lower():
                flag = True
                print(f"INFO :must have title keyword '{each_keyword}' found")
                break

        if not flag:
            for each_keyword in skip_job_keyword_title:
                if each_keyword.lower() in job_title.lower():
                    print(f"INFO :must skip title keyword '{each_keyword}' found..skip this job")
                    return False

        if 2 == len(employees_count_and_type_list) :
            company_type = employees_count_and_type_list[1]

        # if min_employees_count < 5:
        #     print(f"INFO :minimum num of employee not satisfy")
        #     return False
        for x in list_of_must_have_keyword_description:
            if str(x).lower() not in jon_discription_text:
                print(f"INFO :must have keyword {x} not is description hence discard apply")
                return False


        return True
    except BaseException:
        return False


def fill_additional_question(homeAddress=False):
    """
     1 Check form element
     2 count how many element are avaialble with class="jobs-easy-apply-form-section__grouping
     3 loop all the element with class="jobs-easy-apply-form-section__grouping

        4 select 1st child(div class="fb-form-element mt4 jobs-easy-apply-form-element or tabindex="-1"
            this div have 3 child
            label/legend, div, p

            read text from label
            identify tag name or class
            if tag == select:
                read all the option
                select any one option

            elif tag == label:
                match Keyword from dectionary and find Value

    :return:
    """

    line_to_add_in_txt_file = ""
    elements_group_question = driver.find_elements_by_xpath(
        "//div[contains(@class,'jobs-easy-apply-form-section__grouping')]")

    # if Homeaddress page is open only select CIty which is required field
    if homeAddress:
        try:
            all_3_child_elements = elements_group_question[2].find_elements_by_xpath("*[contains(@tabindex,'-1')]/*")
            second_element_of_question = all_3_child_elements[1]
            single_line_input = second_element_of_question.find_element_by_xpath("*//input")
            single_line_input.clear()
            single_line_input.send_keys("Pune, Maharashtra, India")
            time.sleep(1)
            city_list_option = second_element_of_question.find_element_by_xpath(".//li[contains(@role, 'option')][1]")
            ActionChains(driver).move_to_element(city_list_option).click().perform()
            time.sleep(1)
        except BaseException:
            print("Unable to fill Home addresss deatils")
        return True

    for each_ques in elements_group_question:
        time.sleep(1)
        all_3_child_elements = each_ques.find_elements_by_xpath("*[contains(@tabindex,'-1')]/*")
        all_3_child_elements_len = len(all_3_child_elements)

        if all_3_child_elements_len != 0:
            question_text = each_ques.find_element_by_xpath("*[contains(@tabindex,'-1')]/*[1]/*[1]").get_attribute('innerText')
            # question_text = all_3_child_elements[0].get_attribute('innerText')
            second_element_of_question = all_3_child_elements[1]
            tag_name_of_1st_element_of_question = all_3_child_elements[0].tag_name
            element_two_class = all_3_child_elements[1].get_property("className")


            if "fb-single-line-text" in element_two_class:
                single_line_input = second_element_of_question.find_element_by_xpath("*//input")

                if question_text in pre_defined_questions_dict:
                    pre_defined_answer = pre_defined_questions_dict[question_text]
                else:
                    pre_defined_questions_dict[question_text] = None
                    with open("pre_defined_questions.json", "w") as f:
                        json.dump(pre_defined_questions_dict, f, indent=4)
                    pre_defined_answer = 1

                time.sleep(1)
                single_line_input.clear()
                single_line_input.send_keys(pre_defined_answer)
                time.sleep(1)
                print(f"\nQ::{question_text}::{element_two_class}")
                line_to_add_in_txt_file = f"\nQ::{question_text}::{element_two_class}"
            elif "dropdown" in element_two_class:

                select = Select(second_element_of_question.find_element(By.CLASS_NAME, 'fb-dropdown__select'))

                option_text =[]
                for each_option in select.options:
                    option_text.append(each_option.get_attribute("innerText"))

                if question_text in pre_defined_questions_dict_dropdown:
                    if pre_defined_questions_dict_dropdown[question_text] in option_text:
                        pre_defined_answer = pre_defined_questions_dict_dropdown[question_text]
                    else:
                        pre_defined_questions_dict_dropdown[f"{question_text}_NEW"] = option_text
                else:
                    pre_defined_questions_dict_dropdown[question_text] = option_text
                    with open("pre_defined_questions_dropdown.json", "w") as f:
                        json.dump(pre_defined_questions_dict_dropdown, f, indent=4)

                if pre_defined_answer not in option_text:
                    select.select_by_index(1)
                else:
                    select.select_by_visible_text(pre_defined_answer)

                print(f"\nQ::{question_text}::{element_two_class}::{option_text}")
                line_to_add_in_txt_file = f"\nQ::{question_text}::{element_two_class}::{option_text}"

            elif "radio-buttons" in element_two_class:
                radio_options = second_element_of_question.find_elements_by_xpath("*")
                radio_inputs = second_element_of_question.find_elements_by_xpath(".//input")

                radio_option_text = []
                for each_option in radio_options:
                    radio_option_text_temp = each_option.get_attribute('innerText')
                    radio_option_text.append(radio_option_text_temp)

                if question_text in pre_defined_questions_dict_radio:
                    if pre_defined_questions_dict_radio[question_text] in radio_option_text:
                        pre_defined_answer = pre_defined_questions_dict_radio[question_text]
                    else:
                        pre_defined_questions_dict_radio[f"{question_text}_NEW"] = radio_option_text
                else:
                    pre_defined_questions_dict_radio[question_text] = radio_option_text
                    with open("pre_defined_questions_radio.json", "w") as f:
                        json.dump(pre_defined_questions_dict_radio, f, indent=4)
                if pre_defined_answer not in radio_option_text:
                    pre_defined_answer = 'Yes'

                radio_input_yes =  second_element_of_question.find_element_by_xpath(f".//input[@value='{pre_defined_answer}']")
                ActionChains(driver).move_to_element(radio_input_yes).click().perform()
                time.sleep(1)

                print(f"\nQ::{question_text}::{element_two_class}::{radio_option_text}")
                line_to_add_in_txt_file = f"\nQ::{question_text}::{element_two_class}::{radio_option_text}"
            else:
                print(f"new tag element {element_two_class}")
                line_to_add_in_txt_file = f"\nnew tag element {element_two_class}"
        else:
            #This question has difference Dom model, type : "upload Document field "
            all_3_child_elements = each_ques.find_elements_by_xpath("./*[contains(@class,'mt4')]/*")
            element_two_class = all_3_child_elements[2].get_property("className")
            question_text = all_3_child_elements[1].get_attribute('innerText')
            print(f"\nQ::{question_text}::{element_two_class}")
            line_to_add_in_txt_file = f"\nQ::{question_text}::{element_two_class}"

        # Update data in txt file
        with open("Additional_question_data.txt", 'a') as f:
            f.writelines(line_to_add_in_txt_file)


with open('pre_defined_questions.json', 'r') as file1:
    # Reading from json file
    pre_defined_questions_dict = json.load(file1)

with open('pre_defined_questions_dropdown.json', 'r') as file2:
    # Reading from json file
    pre_defined_questions_dict_dropdown = json.load(file2)

with open('pre_defined_questions_radio.json', 'r') as file3:
    # Reading from json file
    pre_defined_questions_dict_radio = json.load(file3)

with open("filtered_job.txt", 'a') as filtered_job:
    filtered_job.write(f"\njob_search_keyword_info: {job_search_keyword_info}   {url}   \n")

#add all convered jobs in text file 'already_Checked_jobs.txt'
with open('already_checked_jobs.txt', 'r') as file4:
    already_checked_jobs_str = file4.read()

if True:
    driver.get(all_url_list[0])
    driver.maximize_window()
    driver.find_element_by_id("cta-modal-header")
    sign_in()
    for each_url in all_url_list:
            try:
                print(f"launch url {each_url}")
                globals
                url = each_url
                driver.get(each_url)
                findAllJobsList()

            except :
                continue


    # minimize_chat_window()

    driver.quit()



