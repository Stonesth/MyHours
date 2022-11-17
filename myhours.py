#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import time

from Tools import tools_v000 as tools
from os.path import dirname
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from keyboard import press

# -7 for the name of this project Myhours
save_path = dirname(__file__)[ : -7]
# save_path = os.path.dirname(os.path.abspath("__file__"))[ : -7]
propertiesFolder_path = save_path + "Properties"

user_text = tools.readProperty(propertiesFolder_path, 'Myhours', 'user_text=')
password_text = tools.readProperty(propertiesFolder_path, 'Myhours', 'password_text=')

dealy_properties = 30

def connectToMyHours() :
    tools.driver.get('https://app.myhours.com')

def enterCredentials() :
    tools.waitLoadingPageByID2(dealy_properties, 'email')
    username = tools.driver.find_element_by_id("email")
    username.send_keys(user_text)

    tools.waitLoadingPageByID2(dealy_properties, 'password')
    password = tools.driver.find_element_by_id("password")
    password.send_keys(password_text)
    password.send_keys(Keys.ENTER)

def startTrack() :
    # Start the chrono
    tools.waitLoadingPageByID2(dealy_properties, 'trackPage')

    # Stop the current Chrono
    try :
        print ("Stop the chrono")
        time.sleep(1)
        tools.waitLoadingPageByID2(dealy_properties, 'stopWorkButton')
        stopTimeStep1 = tools.driver.find_element_by_id('stopWorkButton')
        stopTimeStep1.click()
        time.sleep(1)
    except NoSuchElementException:
        print ("Not possible to stop. because already stopped")

    try:
        tools.waitLoadingPageByID2(dealy_properties, 'startButton')
        timeStep1 = tools.driver.find_element_by_id('startButton')
        timeStep1.click()
        print ("Started a new activity")
    except TimeoutException:
        print ("Clock already started - start new activity")
        tools.waitLoadingPageByID2(dealy_properties, 'startNewButton')
        timeStep1 = tools.driver.find_element_by_id('startNewButton')
        timeStep1.click()

def startTrackWithDescription(jira, description, epic_link) :
    tools.waitLoadingPageByXPATH2(10, '//*[@id="trackPage"]/div[5]/div/div[2]/div')
    
    time.sleep(2)
    # Need to check if already a track without description is started
    if (tools.waitLoadingPageByXPATH2(10, '//*[@id="trackPage"]/div[5]/div/div[2]/div/log-display/div/div[1]/div/div[1]/div/h5/small/i')) :
        description_text = tools.driver.find_element_by_xpath('//*[@id="trackPage"]/div[5]/div/div[2]/div/log-display/div/div[1]/div/div[1]/div/h5/small/i')
        print('Description = ' + description_text.text)
        if (description_text.text == 'Empty description') :
            print("Already started => don't restart a new time")
        else :
            print("Don't have an empty description => start a new track")
            startTrack()
    else :
        startTrack()

    time.sleep(2)
    # Click on the current run
    print ("Click on the current run")
    timeStep1 = tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]')
    timeStep1.click()
    
    # If we see the "Edit time log", we are already on the edit of the time
    if (tools.waitLoadingPageByXPATH2(10, '//*[@id="logFormWrapper"]/form/div/div[1]/h4')) :
        time.sleep(2)
        # Do the modification of the track
        print ("Do the modification of the track")
        modifyTrack(jira, description, epic_link)
    else :
        print ("Try to overide the class and removed the string hover-child")
        if (tools.waitLoadingPageByXPATH2(10, '/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]/div[1]/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/a[1]')) :
            tools.driver.execute_script("arguments[0].setAttribute('class', 'mr-3 small ng-scope')", tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]/div[1]/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/a[1][@class="hover-child mr-3 small ng-scope"]'))
            time.sleep(2)

        if (tools.waitLoadingPageByXPATH2(10, '//*[@id="editLog"]')) :
            timeStep1 = tools.driver.find_element_by_xpath('//*[@id="editLog"]')
            timeStep1.click()   
            time.sleep(2)
            # Do the modification of the track
            print ("Do the modification of the track")
            modifyGroupTrack(jira, description, epic_link)
        
    # To let the time to refresh the page
    time.sleep(2)    

def startTrackWithDescription_1(jira, description, epic_link) :
    tools.waitLoadingPageByID2(10, 'timeStep1')
    timeStep1 = tools.driver.find_element_by_id('timeStep1')

    # Stop the current run
    stopCurrentLog = tools.driver.find_element_by_id('stopCurrentLog')
    stopCurrentLog.click()
    
    # Place this line because there is a refresh of the page after stopping the currentLog
    tools.waitLoadingPageByID2(10, 'timeStep1')
    time.sleep(1)
    
    # Find all the different entry
    listAppWrapper = tools.driver.find_elements_by_xpath("//div[@class = 'd-flex flex-column my-1 col-12 col-xl-7']")

    j = 1
    found = False
    for i in listAppWrapper:
        j = j + 1
        if (i.text.find(description) >= 0) :
            found = True
            break
    
    # if found click to Resume button, else create a new track
    if (found) :
       resumeButton = tools.driver.find_element_by_xpath("/html/body/div[1]/div/div/layout/div/div[2]/div/div/compact/div/div[2]/log-list/div["+str(j)+"]/div/div/div[3]/log-action-toolbar/div/button[1]/span")
       resumeButton.click()
    else :
       timeStep1.click()
       # start a new track
       startTrack()
       modifyTrack(jira, description, epic_link)

    # To let the time to refresh the page
    time.sleep(2)

def modifyTrack(jira, description, epic_link) :
    # Project
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogProjectInput"]/div/div[1]/div/div/div/div/div[1]/input')
    projectLookup = tools.driver.find_element_by_xpath('//*[@id="logFormEditLogProjectInput"]/div/div[1]/div/div/div/div/div[1]/input')
    time.sleep(1)
    projectLookup.click()
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogProjectInput"]/div[1]/div[1]/div/div/div/div/div[1]/input')  
    time.sleep(2)
    projectInput = tools.driver.find_element_by_xpath('//*[@id="logFormEditLogProjectInput"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    # Select the Project
    time.sleep(1)
    projectInput.click()
    projectInput.send_keys(Keys.ENTER)


    # time.sleep(1)
    # projectInput.click()
    
    # time.sleep(1)                                    
    # tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div[1]')
    # time.sleep(1)
    # select = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div[1]')
    # select.click()

    # press('enter')
    
    time.sleep(2)

    # Task
    tools.waitLoadingPageByID2(dealy_properties, 'trackPageEditFormTask')
    taskLookup = tools.driver.find_element_by_id('trackPageEditFormTask')
    taskLookup.click()

    time.sleep(1)
    
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="trackPageEditFormTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="trackPageEditFormTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(jira)
    time.sleep(1) # To fast if not present
    projectInput.send_keys(Keys.ENTER)
    
    # TAG
    tools.waitLoadingPageByID2(dealy_properties, 'logFormEditLogTagsInput')
    tagLookup = tools.driver.find_element_by_id('logFormEditLogTagsInput')
    tagLookup.click()

    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogTagsInput"]/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element_by_xpath('//*[@id="logFormEditLogTagsInput"]/div[1]/div/div[1]/input')
    tagInput.send_keys('JIRA')
    time.sleep(2)
    tagInput.send_keys(Keys.ENTER)

    # Description
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="editor"]/div[1]')
    logAddEditDescription = tools.driver.find_element_by_xpath('//*[@id="editor"]/div[1]')
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'saveTimeLogBtn')
    editLog = tools.driver.find_element_by_id('saveTimeLogBtn')
    editLog.click()

def modifyTrack_1(jira, description, epic_link) :
    # Edit the button
    tools.waitLoadingPageByID2(dealy_properties, 'runningEdit')
    runningEdit = tools.driver.find_element_by_id('runningEdit')
    runningEdit.click()

    # Project
    tools.waitLoadingPageByID2(dealy_properties, 'projectLookup')
    projectLookup = tools.driver.find_element_by_id('projectLookup')
    projectLookup.click()
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')  
    time.sleep(2)
    projectInput = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    time.sleep(2)
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div') 
    time.sleep(2)
    projectList = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')
    print('projectList.text = ' + projectList.text)
    if projectList.text == 'None found. Press Enter to create one.' :
        print ("No project found => create a new one")
        # Create a new Project        
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[3]/div/div[1]/button') 
        create_button = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[3]/div/div[1]/button')
        create_button.click()

        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        select_society_input = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/p')
        select_society_input.click()
        
        # Select the society Delta Lloyd Life
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society = tools.driver.find_element_by_xpath('/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society.click()

        # Click into the button Create
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        create_button2 = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div/div[3]/button')
        create_button2.click()
    else :        
        ## Select Project
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')  
        projectSelect = tools.driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')
        projectSelect.click()

    # Task
    tools.waitLoadingPageByID2(dealy_properties, 'taskLookupEdit')
    taskLookup = tools.driver.find_element_by_id('taskLookupEdit')
    taskLookup.click()

    time.sleep(1)
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="taskInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="taskInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys('JIRA')
    time.sleep(1) # To fast if not present
    projectInput.send_keys(Keys.ENTER)

    ## Select Task
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    projectSelect = tools.driver.find_element_by_xpath('//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    projectSelect.click()
    
    # TAG
    tools.waitLoadingPageByID2(dealy_properties, 'tagSelect')
    tagLookup = tools.driver.find_element_by_id('tagSelect')
    tagLookup.click()

    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element_by_xpath('//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    tagInput.send_keys(jira)
    time.sleep(2)
    tagInput.send_keys(Keys.ENTER)

    # Billable time     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')  
    billable_time = tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')
    # billable_time.send_keys(Keys.SPACE)

    # Description
    tools.waitLoadingPageByID2(dealy_properties, 'logAddEditDescription')
    logAddEditDescription = tools.driver.find_element_by_id('logAddEditDescription')
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'editLog')
    editLog = tools.driver.find_element_by_id('editLog')
    editLog.click()

def modifyGroupTrack(jira, description, epic_link) :
    # Project
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="projectInputId"]/div/div[1]/div/div/div/div/div[1]/input')
    projectLookup = tools.driver.find_element_by_xpath('//*[@id="projectInputId"]/div/div[1]/div/div/div/div/div[1]/input')
    time.sleep(1)
    projectLookup.click()
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="projectInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')  
    time.sleep(2)
    projectInput = tools.driver.find_element_by_xpath('//*[@id="projectInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    # Select the Project
    time.sleep(1)
    projectInput.click()
    projectInput.send_keys(Keys.ENTER)    
    time.sleep(2)

    # Task
    tools.waitLoadingPageByID2(dealy_properties, 'editLogTask')
    taskLookup = tools.driver.find_element_by_id('editLogTask')
    taskLookup.click()

    time.sleep(1)
    
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="editLogTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="editLogTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(jira)
    time.sleep(1) # To fast if not present
    projectInput.send_keys(Keys.ENTER)
    
    # TAG
    tools.waitLoadingPageByID2(dealy_properties, 'tagSelect')
    tagLookup = tools.driver.find_element_by_id('tagSelect')
    tagLookup.click()

    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element_by_xpath('//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    tagInput.send_keys('JIRA')
    time.sleep(2)
    tagInput.send_keys(Keys.ENTER)

    # Description
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="editor"]/div[1]')
    logAddEditDescription = tools.driver.find_element_by_xpath('//*[@id="editor"]/div[1]')
    logAddEditDescription.click()
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'editLogSaveButton')
    editLog = tools.driver.find_element_by_id('editLogSaveButton')
    editLog.click()

# # For testing purposec
# # Open Browser
# tools.openBrowserChrome()
# connectToMyHours()
# enterCredentials()
# startTrackWithDescription('TOS-4515', 'la description', 'Run Life')