from os import startfile
from selenium import webdriver
import json

# Open incognito chrome session and navigate to UBC page
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Chrome(executable_path = "D:\chromedriver_win32\chromedriver.exe", chrome_options=options)
driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments")


# This function clicks every subject link, then every course link in every subject link, and every 
# section link in every course, and scrapes relevant data for 2021 winter session and stores it in a json file
def scrape_courses():

    all_courses = []

    size_subjects = len(driver.find_elements_by_class_name("section1")) + len(driver.find_elements_by_class_name("section2"))
    
    for i in range(size_subjects):

        subject_xpath = "/html/body/div[2]/div[4]/table/tbody/tr["+str(i+1)+"]/td[1]/a"

        try:  
            subject_link = driver.find_element_by_xpath(subject_xpath)
            subject_link.click()

            size_courses = len(driver.find_elements_by_class_name("section1")) + len(driver.find_elements_by_class_name("section2"))

            for k in range(size_courses):
                course_xpath = "/html/body/div[2]/div[4]/table/tbody/tr["+str(k+1)+"]/td[1]/a" if size_courses > 1 else "/html/body/div[2]/div[4]/table/tbody/tr/td[1]/a"

                try:
                    course_link = driver.find_element_by_xpath(course_xpath)
                    course_link.click()
                    
                    size_sections = len(driver.find_elements_by_class_name("section1")) + len(driver.find_elements_by_class_name("section2"))
                    
                    try:
                        prereq = driver.find_element_by_xpath('/html/body/div[2]/div[4]/p[3]').text
                    except:
                        prereq = ""

                    for j in range(size_sections):
                        
                        section_xpath = "/html/body/div[2]/div[4]/table[2]/tbody/tr["+str(j+1)+"]/td[2]/a" if size_sections > 1 else "/html/body/div[2]/div[4]/table[2]/tbody/tr/td[2]/a"
                        
                        try:
                            section_link = driver.find_element_by_xpath(section_xpath)
                            section_link.click()

                            try:
                                subject = driver.find_element_by_xpath('/html/body/div[2]/ul/li[3]/a').text
                            except:
                                subject = ""

                            
                            try:
                                code = driver.find_element_by_xpath('/html/body/div[2]/ul/li[4]/a').text
                            except:
                                code = ""

                            
                            try:
                                section = driver.find_element_by_xpath('/html/body/div[2]/ul/li[5]').text
                            except:
                                section = ""
                            # Section is the whole course code (ie. CHEM 123 101), so need to isolate just the section (ie. 101)
                            if len(section) > 0:
                                section = section.split()[2]
                            
                            
                            try:
                                title = driver.find_element_by_xpath('/html/body/div[2]/div[4]/h5').text
                            except:
                                title = ""
                            
                            
                            try:
                                term = driver.find_element_by_xpath('/html/body/div[2]/div[4]/b[1]').text
                            except:
                                term = ""

                            
                            try:
                                summary = driver.find_element_by_xpath('/html/body/div[2]/div[4]/p[1]').text
                            except:
                                summary = ""

                            
                            try:
                                credits = driver.find_element_by_xpath('/html/body/div[2]/div[4]/p[2]').text
                            except:
                                credits = ""

                            try:
                                days = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[2]/tbody/tr/td[2]').text
                            except:
                                days = ""

                            try:
                                start = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[2]/tbody/tr/td[3]').text
                            except:
                                start = ""

                            try:
                                end = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[2]/tbody/tr/td[4]').text
                            except:
                                end = ""

                            try:
                                building = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[2]/tbody/tr/td[5]').text
                            except:
                                building = ""

                            try:
                                room = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[2]/tbody/tr/td[6]/a').text
                            except:
                                room = ""

                            try:
                                instructor = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table[3]/tbody/tr/td[2]/a').text
                            except:
                                instructor = ""

                            
                            course_dict = {
                                "course_code": code,
                                "course_title": title,
                                "section": section,
                                "subject": subject,
                                "summary": summary,
                                "credits": credits,
                                "prereqs": prereq,
                                "term": term,
                                "days": days,
                                "start": start,
                                "end": end,
                                "building": building,
                                "room": room,
                                "instructor": instructor
                            }
                            
                            
                            print(course_dict)
                            all_courses.append(course_dict)
                            

                            driver.back()
                        except:
                            continue

                    driver.back()
                except:
                    continue

            driver.back()
        except:
            continue


    return all_courses


data = scrape_courses()
with open('winter2021pt2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)