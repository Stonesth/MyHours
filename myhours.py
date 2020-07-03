import os
import time

from Tools import tools_v000 as tools
from os.path import dirname
from selenium.webdriver.common.keys import Keys

# -7 for the name of this project Myhours
save_path = dirname(__file__)[ : -7]
propertiesFolder_path = save_path + "Properties"

user_text = tools.readProperty(propertiesFolder_path, 'Myhours', 'user_text=')
password_text = tools.readProperty(propertiesFolder_path, 'Myhours', 'password_text=')

def connectToMyHours() :
    tools.driver.get('https://app.myhours.com')

def enterCredentials() :
    tools.waitLoadingPageByID('email')
    username = tools.driver.find_element_by_id("email")
    username.send_keys(user_text)

    tools.waitLoadingPageByID('password')
    password = tools.driver.find_element_by_id("password")
    password.send_keys(password_text)
    password.send_keys(Keys.ENTER)

def startTrack() :
    # Start the chrono
    tools.waitLoadingPageByID('timeStep1')
    timeStep1 = tools.driver.find_element_by_id('timeStep1')
    timeStep1.click()

def modifyTrack(jira, description, epic_link) :
    # Edit the button
    tools.waitLoadingPageByID('runningEdit')
    runningEdit = tools.driver.find_element_by_id('runningEdit')
    runningEdit.click()

    # Project
    tools.waitLoadingPageByID('projectLookup')
    projectLookup = tools.driver.find_element_by_id('projectLookup')
    projectLookup.click()

    tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')  
    projectInput = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    time.sleep(1)

    tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div') 
    projectList = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')
    if projectList.text == 'No projects found.' :
        print ("No project found => create a new one")
        # Create a new Project        
        tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[3]/div/div[1]/button') 
        create_button = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[3]/div/div[1]/button')
        create_button.click()

        tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        select_society_input = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/p')
        select_society_input.click()
                                      
        tools.waitLoadingPageByXPATH('/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society = tools.driver.find_element_by_xpath('/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society.click()

        tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        create_button2 = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div/div[3]/button')
        create_button2.click()
    else :        
        ## Select Project
        tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')  
        projectSelect = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')
        projectSelect.click()

    # Task
    tools.waitLoadingPageByID('taskLookup')
    taskLookup = tools.driver.find_element_by_id('taskLookup')
    taskLookup.click()

    time.sleep(1)

    tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')  
    projectInput = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')
    projectInput.send_keys('JIRA')

    ## Select Task
    tools.waitLoadingPageByXPATH('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')  
    projectSelect = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')
    projectSelect.click()
    
    # TAG
    tools.waitLoadingPageByID('tagSelect')
    tagLookup = tools.driver.find_element_by_id('tagSelect')
    tagLookup.click()

    tools.waitLoadingPageByXPATH('/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[3]/div/tag-select/div/div/div/div/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[3]/div/tag-select/div/div/div/div/div[1]/div/div[1]/input')
    tagInput.send_keys(jira)
    tagInput.send_keys(Keys.ENTER)

    # Billable time     
    tools.waitLoadingPageByXPATH('/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')  
    billable_time = tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')
    # billable_time.send_keys(Keys.SPACE)

    # Description
    tools.waitLoadingPageByID('logAddEditDescription')
    logAddEditDescription = tools.driver.find_element_by_id('logAddEditDescription')
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID('editLog')
    editLog = tools.driver.find_element_by_id('editLog')
    editLog.click()