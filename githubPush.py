from github import Github;from github import InputGitTreeElement;
from UserPass_Encrypt import *;from datetime import date;
from os import listdir;import os;from os.path import join;

Decrypted_user = base64.b64decode(user).decode("utf-8");Decrypted_password = base64.b64decode(password).decode("utf-8");
g = Github(Decrypted_user,Decrypted_password);

repo = g.get_user().get_repo('FMON_DataManagement'); # repo name
file_list = ['FMON_performanceData.csv','T1_FMON_performanceData.csv'];file_names = [];

for item in os.listdir('.\\figures'):
    file_list.append(os.path.join('figures\\', item));
for item in file_list:
    if item.endswith('.png'):
        pngSplit = item.split('\\')
        pngName = 'individual_MiceFigures' + '/' + str(pngSplit[1])
        file_names.append(pngName)
    else:
        file_names.append(item)


#file_names = ['FMON_performanceData.csv','T1_FMON_performanceData.csv'];
#for item in os.listdir('.\\figures'):
 #   file_list.append(os.path.join('figures\\', item));
  #  file_names.append(item);

today = date.today();commit_message = 'FMON Python push (last updated: '+str(today)+')';
master_ref = repo.get_git_ref('heads/main');
master_sha = master_ref.object.sha;
base_tree = repo.get_git_tree(master_sha);

element_list = list();
for i, entry in enumerate(file_list):
    with open(entry) as input_file:
        data = input_file.read();
    if entry.endswith('.png'): # images must be encoded
        data = base64.b64encode(data);
    element = InputGitTreeElement(file_names[i], '100644', 'blob', data);
    element_list.append(element);

tree = repo.create_git_tree(element_list, base_tree);
parent = repo.get_git_commit(master_sha);
commit = repo.create_git_commit(commit_message, tree, [parent]);
master_ref.edit(commit.sha);

for entry in file_list:
    with open(entry, 'rb') as input_file:
        data = input_file.read()
    if entry.endswith('.png'):
        pushSplit = entry.split('\\')
        pngPushName = 'individual_MiceFigures' + '/' + str(pushSplit[1])
        old_file = repo.get_contents(pngPushName)
        commit = repo.update_file( pngPushName,'FMON Python push (png updated: '+str(today)+')', data, old_file.sha)

print('commit successful!');