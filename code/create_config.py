import configparser

def create_config():
    config = configparser.ConfigParser()

    #add sections and key value pairs
    config['file_paths'] = {
        'concept_folder_path': '/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/datastores/concepts',
        'game_logs_folder': '/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/extracted',
        'concept_names_path': '/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/datastores/constructs.json',
        'function_selector_prompt_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/prompts/function_selector.txt',
        'task_description_prompt_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/prompts/task_description.txt',
        'chat_history_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/datastores/chat_history_test_block.json',
        'blocked_locations_file':'/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/datastores/blocked_locations_testing.json',
    }

    with open('/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/config.ini','w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    create_config()
    print('The config file has been dumped !!')