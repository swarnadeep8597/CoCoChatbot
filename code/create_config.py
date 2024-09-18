import configparser

def create_config():
    config = configparser.ConfigParser()

    #add sections and key value pairs
    config['file_paths'] = {
        'concept_folder_path': '/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/datastores/concepts',
        'game_logs_folder': '/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/extracted',
        'concept_names_path': '/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/datastores/constructs.json',
        'function_selector_prompt_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/prompts/function_selector.txt',
        'task_description_prompt_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/prompts/task_description.txt',
        'chat_history_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/datastores/chat_history.json',
        'blocked_locations_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/datastores/blocked_locations.json',
    }

    with open('/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/config.ini','w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    create_config()
    print('The config file has been dumped !!')