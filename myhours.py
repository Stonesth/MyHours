#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import time

from Tools import tools_v000 as tools
from os.path import dirname
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from keyboard import press
from selenium.webdriver.support import expected_conditions as EC

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
    tools.waitLoadingPageByID2(dealy_properties, 'username-field') # change since the 22-05-2024 : email
    username = tools.driver.find_element(By.ID, "username-field") # change since the 22-05-2024 : email
    username.send_keys(user_text)

    tools.waitLoadingPageByID2(dealy_properties, 'password-field') # change since the 22-05-2024 : password
    password = tools.driver.find_element(By.ID, "password-field") # change since the 22-05-2024 : password
    password.send_keys(password_text)
    password.send_keys(Keys.ENTER)

def startTrack() :
    # Start the chrono
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/mh-header/div/h1')

    # Since the 22-05-2024 it's not possible to stop the current chrono
    # We need to start a new one each time


    # # Stop the current Chrono
    # try :
    #     print ("Stop the chrono")
    #     time.sleep(10)

    #     # To avoid the problem of the button not clickable.
    #     # we need to change the style visible from hidden to visible.
    #     # /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div/div/div[1]/div/div[2]/mh-log-item-toolbar/div
    #     tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div/div/div[1]/div/div[2]/mh-log-item-toolbar/div')
    #     time.sleep(1)
    #     stopTimeStep1 = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div/div/div[1]/div/div[2]/mh-log-item-toolbar/div')
    #     tools.driver.execute_script("arguments[0].setAttribute('style', 'visibility: visible;')", stopTimeStep1)

    #     time.sleep(5)
    #     tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="stopWorkButton"]')
    #     stopTimeStep1 = tools.driver.find_element(By.XPATH, '//*[@id="stopWorkButton"]') # change since the 22-05-2024 : stopTimeStep1
    #     wait = tools.WebDriverWait(tools.driver, 10)  # Attendre jusqu'à 10 secondes
    #     stopTimeStep1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="stopWorkButton"]')))
    #     stopTimeStep1.click()
    #     time.sleep(1)
    # except NoSuchElementException:
    #     print ("Not possible to stop. because already stopped")

    try:
        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="startButton"]')
        timeStep1 = tools.driver.find_element(By.XPATH, '//*[@id="startButton"]') # change since the 22-05-2024 : timeStep1
        timeStep1.click()
        print ("Started a new activity")
    except TimeoutException:
        print ("Clock already started - start new activity")
        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="startButton"]')
        timeStep1 = tools.driver.find_element(By.XPATH, '//*[@id="startButton"]') # change since the 22-05-2024 : timeStep1
        # tools.waitLoadingPageByID2(dealy_properties, 'startNewButton') # change since the 22-05-2024 : timeStep1
        # timeStep1 = tools.driver.find_element(By.ID, 'startNewButton') # change since the 22-05-2024 : timeStep1
        timeStep1.click()

def startTrackWithDescription(jira, description, epic_link) :
    tools.waitLoadingPageByXPATH2(20, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]') # change since the 22-05-2024 : timeStep1
    
    time.sleep(2)
    # Need to check if already a track without description is started
    if (tools.waitLoadingPageByXPATH2(10, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div/i')) :
        description_text = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div/i')
        print('Description = ' + description_text.text)
        if (description_text.text == 'Add project, task, and other details') :
            print("Already started => don't restart a new time")
        else :
            print("Don't have an empty description => start a new track")
            startTrack()
    else :
        startTrack()

    time.sleep(2)
    # Click on the current run
    print ("Click on the current run")
    tools.waitLoadingPageByXPATH2(10, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div')
    timeStep1 = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[1]/div/div')
    timeStep1.click()
    
    # If we see the "Edit time log", we are already on the edit of the time
    # tools.waitLoadingPageByXPATH2(10, '//*[@id="logBulkEditFormWrapper"]')
    # Do the modification of the track
    print ("Do the modification of the track")
    modifyTrack(jira, description, epic_link)
    # if (tools.waitLoadingPageByXPATH2(10, '//*[@id="logBulkEditFormWrapper"]/form/div[1]/div/h5')) :
    #     time.sleep(2)
    #     # Do the modification of the track
    #     print ("Do the modification of the track")
    #     modifyTrack(jira, description, epic_link)
    # else :
    #     print ("Try to overide the class and removed the string hover-child")
    #     # if (tools.waitLoadingPageByXPATH2(10, '/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]/div[1]/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/a[1]')) :
    #     #     tools.driver.execute_script("arguments[0].setAttribute('class', 'mr-3 small ng-scope')", tools.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]/div[1]/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/a[1][@class="hover-child mr-3 small ng-scope"]'))
    #     #     time.sleep(2)

    #     if (tools.waitLoadingPageByXPATH2(10, '//*[@id="logBulkEditFormWrapper"]')) : # change since the 22-05-2024
    #         timeStep1 = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]') # change since the 22-05-2024
    #         timeStep1.click()   
    #         time.sleep(2)
    #         # Do the modification of the track
    #         print ("Do the modification of the track")
    #         modifyGroupTrack(jira, description, epic_link)
        
    # To let the time to refresh the page
    time.sleep(2)    

def startTrackWithDescription_1(jira, description, epic_link) :
    tools.waitLoadingPageByID2(10, 'timeStep1')
    timeStep1 = tools.driver.find_element(By.ID, 'timeStep1')

    # Stop the current run
    stopCurrentLog = tools.driver.find_element(By.ID, 'stopCurrentLog')
    stopCurrentLog.click()
    
    # Place this line because there is a refresh of the page after stopping the currentLog
    tools.waitLoadingPageByID2(10, 'timeStep1')
    time.sleep(1)
    
    # Find all the different entry
    listAppWrapper = tools.driver.find_elements(By.XPATH, "//div[@class = 'd-flex flex-column my-1 col-12 col-xl-7']")

    j = 1
    found = False
    for i in listAppWrapper:
        j = j + 1
        if (i.text.find(description) >= 0) :
            found = True
            break
    
    # if found click to Resume button, else create a new track
    if (found) :
       resumeButton = tools.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/layout/div/div[2]/div/div/compact/div/div[2]/log-list/div["+str(j)+"]/div/div/div[3]/log-action-toolbar/div/button[1]/span")
       resumeButton.click()
    else :
       timeStep1.click()
       # start a new track
       startTrack()
       modifyTrack(jira, description, epic_link)

    # To let the time to refresh the page
    time.sleep(2)

def modifyTrack(jira, description, epic_link) :

    # Need to test if we are in bulk edit or not
    if (tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogProjectInput"]')) :
        print ("Select the project in a single track")
        # Project                                           
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/sds-modal[1]/div[2]/div/div/div[1]/mh-log-form/div/form/div[2]/div[1]/div/div[1]/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')  
        projectLookup = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/sds-modal[1]/div[2]/div/div/div[1]/mh-log-form/div/form/div[2]/div[1]/div/div[1]/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        time.sleep(2)
        projectLookup.click()
                                                   
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/sds-modal[1]/div[2]/div/div/div[1]/mh-log-form/div/form/div[2]/div[1]/div/div[1]/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')  
        time.sleep(2)
        projectInput = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/sds-modal[1]/div[2]/div/div/div[1]/mh-log-form/div/form/div[2]/div[1]/div/div[1]/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        projectInput.send_keys(epic_link)
        time.sleep(5)
        projectInput.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(2)

        print ("Select the task")
        # Task
        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="trackPageEditFormTask"]/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        taskLookup = tools.driver.find_element(By.XPATH, '//*[@id="trackPageEditFormTask"]/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div/input')
        taskLookup.click()

        time.sleep(1)
        
        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="trackPageEditFormTask"]/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        projectInput = tools.driver.find_element(By.XPATH, '//*[@id="trackPageEditFormTask"]/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        projectInput.send_keys(jira)
        time.sleep(1) # To fast if not present
        projectInput.send_keys(Keys.ENTER)
    
        print ("Select the TAG")
        # TAG
        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogTagsInput"]/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')
        tagLookup = tools.driver.find_element(By.XPATH, '//*[@id="logFormEditLogTagsInput"]/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]')
        tagLookup.click()

        tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogTagsInput"]/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')  
        tagInput = tools.driver.find_element(By.XPATH, '//*[@id="logFormEditLogTagsInput"]/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')
        tagInput.send_keys('JIRA')
        time.sleep(2)
        tagInput.send_keys(Keys.ENTER)


    else :
        print ("Select the project in a group track")
        # Project
        ##########################################################
        # For the moment there is an issue in the site of MyHours
        # He don't recognize old project.
        # Need to reactivate this section when the issue is fixed
        ##########################################################
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[3]/div/div/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')  
        # projectLookup = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[3]/div/div/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # time.sleep(2)
        # projectLookup.click()
                                                   
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[3]/div/div/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')  
        # time.sleep(2)
        # projectInput = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[3]/div/div/mh-project-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # projectInput.send_keys(epic_link)
        # time.sleep(2)
        # projectInput.send_keys(Keys.ENTER)
        
        # time.sleep(1)
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[4]/div/div/mh-project-task-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # taskLookup = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[4]/div/div/mh-project-task-select/mh-select-box-toolbar-actions/dx-select-box/div/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # taskLookup.click()

        print ("Select the task")
        # Task
        ##########################################################
        # For the moment there is an issue in the site of MyHours
        # He don't recognize old project.
        # Need to reactivate this section when the issue is fixed
        ##########################################################
        # time.sleep(5)
        
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[4]/div/div/mh-project-task-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # projectInput = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[4]/div/div/mh-project-task-select/mh-select-box-toolbar-actions/dx-select-box/div[1]/div[1]/div/div/div/dx-text-box/div/div[1]/input')
        # projectInput.send_keys(jira)
        # time.sleep(1) # To fast if not present
        # projectInput.send_keys(Keys.ENTER)
        
        print ("Select the TAG")
        # TAG
        ##########################################################
        # For the moment there is an issue in the site of MyHours
        # He don't recognize old project.
        # Need to reactivate this section when the issue is fixed
        ##########################################################
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[7]/div/mh-tags-select/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')  
        # tagLookup = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[7]/div/mh-tags-select/dx-tag-box/div/div[1]/div/div/dx-text-box/div/div[1]/input')
        # tagLookup.click()
        # tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logBulkEditFormWrapper"]/form/div[7]/div/mh-tags-select/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')  
        # tagInput = tools.driver.find_element(By.XPATH, '//*[@id="logBulkEditFormWrapper"]/form/div[7]/div/mh-tags-select/dx-tag-box/div[1]/div[1]/div/div/dx-text-box/div/div[1]/input')
        # tagInput.send_keys('JIRA')
        # time.sleep(2)
        # tagInput.send_keys(Keys.ENTER)
   
    # Description
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="logFormEditLogNoteInput"]')
    logAddEditDescription = tools.driver.find_element(By.XPATH, '//*[@id="logFormEditLogNoteInput"]')
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'saveTimeLogBtn')
    editLog = tools.driver.find_element(By.ID, 'saveTimeLogBtn')
    editLog.click()

def modifyTrack_1(jira, description, epic_link) :
    # Edit the button
    tools.waitLoadingPageByID2(dealy_properties, 'runningEdit')
    runningEdit = tools.driver.find_element(By.ID, 'runningEdit')
    runningEdit.click()

    # Project
    tools.waitLoadingPageByID2(dealy_properties, 'projectLookup')
    projectLookup = tools.driver.find_element(By.ID, 'projectLookup')
    projectLookup.click()
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')  
    time.sleep(2)
    projectInput = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div[1]/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    time.sleep(2)
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div') 
    time.sleep(2)
    projectList = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')
    print('projectList.text = ' + projectList.text)
    if projectList.text == 'None found. Press Enter to create one.' :
        print ("No project found => create a new one")
        # Create a new Project        
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[3]/div/div[1]/button') 
        create_button = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[3]/div/div[1]/button')
        create_button.click()

        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        select_society_input = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/p')
        select_society_input.click()
        
        # Select the society Delta Lloyd Life
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society = tools.driver.find_element(By.XPATH, '/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div')
        select_society.click()

        # Click into the button Create
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div/div/div[3]/button') 
        create_button2 = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div/div[3]/button')
        create_button2.click()
    else :        
        ## Select Project
        tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')  
        projectSelect = tools.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div')
        projectSelect.click()

    # Task
    tools.waitLoadingPageByID2(dealy_properties, 'taskLookupEdit')
    taskLookup = tools.driver.find_element(By.ID, 'taskLookupEdit')
    taskLookup.click()

    time.sleep(1)
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="taskInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput = tools.driver.find_element(By.XPATH, '//*[@id="taskInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys('JIRA')
    time.sleep(1) # To fast if not present
    projectInput.send_keys(Keys.ENTER)

    ## Select Task
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    projectSelect = tools.driver.find_element(By.XPATH, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    projectSelect.click()
    
    # TAG
    tools.waitLoadingPageByID2(dealy_properties, 'tagSelect')
    tagLookup = tools.driver.find_element(By.ID, 'tagSelect')
    tagLookup.click()

    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element(By.XPATH, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    tagInput.send_keys(jira)
    time.sleep(2)
    tagInput.send_keys(Keys.ENTER)

    # Billable time     
    tools.waitLoadingPageByXPATH2(dealy_properties, '/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')  
    billable_time = tools.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/log-edit-modal/div[2]/form/div[4]/div[2]/div/input')
    # billable_time.send_keys(Keys.SPACE)

    # Description
    tools.waitLoadingPageByID2(dealy_properties, 'logAddEditDescription')
    logAddEditDescription = tools.driver.find_element(By.ID, 'logAddEditDescription')
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'editLog')
    editLog = tools.driver.find_element(By.ID, 'editLog')
    editLog.click()

def modifyGroupTrack(jira, description, epic_link) :
    # Project
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="projectInputId"]/div/div[1]/div/div/div/div/div[1]/input')
    projectLookup = tools.driver.find_element(By.XPATH, '//*[@id="projectInputId"]/div/div[1]/div/div/div/div/div[1]/input')
    time.sleep(1)
    projectLookup.click()
                                                     
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="projectInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')  
    time.sleep(2)
    projectInput = tools.driver.find_element(By.XPATH, '//*[@id="projectInputId"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(epic_link)

    # Select the Project
    time.sleep(1)
    projectInput.click()
    projectInput.send_keys(Keys.ENTER)    
    time.sleep(2)

    # Task
    tools.waitLoadingPageByID2(dealy_properties, 'editLogTask')
    taskLookup = tools.driver.find_element(By.ID, 'editLogTask')
    taskLookup.click()

    time.sleep(1)
    
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="editLogTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput = tools.driver.find_element(By.XPATH, '//*[@id="editLogTask"]/div[1]/div[1]/div/div/div/div/div[1]/input')
    projectInput.send_keys(jira)
    time.sleep(1) # To fast if not present
    projectInput.send_keys(Keys.ENTER)
    
    # TAG
    tools.waitLoadingPageByID2(dealy_properties, 'tagSelect')
    tagLookup = tools.driver.find_element(By.ID, 'tagSelect')
    tagLookup.click()

    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')  
    tagInput = tools.driver.find_element(By.XPATH, '//*[@id="tagSelect"]/div[1]/div/div[1]/input')
    tagInput.send_keys('JIRA')
    time.sleep(2)
    tagInput.send_keys(Keys.ENTER)

    # Description
    tools.waitLoadingPageByXPATH2(dealy_properties, '//*[@id="editor"]/div[1]')
    logAddEditDescription = tools.driver.find_element(By.XPATH, '//*[@id="editor"]/div[1]')
    logAddEditDescription.click()
    logAddEditDescription.send_keys(description)
    
    # editLog
    tools.waitLoadingPageByID2(dealy_properties, 'editLogSaveButton')
    editLog = tools.driver.find_element(By.ID, 'editLogSaveButton')
    editLog.click()

# # For testing purposec
# # Open Browser
# tools.openBrowserChrome()
# connectToMyHours()
# enterCredentials()
# startTrackWithDescription('TOS-4515', 'la description', 'Run Life')