
clc; close all; clear;

projectDirs = get_project_dirs;
subjects = {getfolders(projectDirs.simulations).name};

% select trc trial path for scaling
[filename, filepath] = uigetfile([projectDirs.simulations fp  '*.*'],'select trc file to use for scalling');
static_trc_path = [filepath filename];

% find sessionDir and subject name from trc path
sessionDir = DirUp(static_trc_path,2);
[~,session_name] = DirUp(sessionDir,1);
[~,subject_name] = DirUp(sessionDir,2);
cd(sessionDir)

original_model_path = [sessionDir fp 'FINAL_PERSONALISEDTORSIONS.osim'];
setupScaleXmlPath = projectDirs.setupFiles.Scale;
bodymass = get_body_mass_from_csv_file(sessionDir);

% scale model
scaled_model_path_static = runScale(static_trc_path,original_model_path,setupScaleXmlPath,bodymass);

model_name = ['FINAL_PERSONALISEDTORSIONS_scaled.osim'];
iSub = 1;

current_subject = subjects{iSub};
sessionDir      = [projectDirs.simulations fp current_subject fp 'pre'];
[~,session_name] = DirUp(sessionDir,1);
[~,subject_name] = DirUp(sessionDir,2);
cd(sessionDir)

disp(current_subject)

% get setup file directories
[IKsetup, IDsetup, SOsetup, SOactuators, JRLsetup, MAsetup, MEsetup,RRAsetup] = get_setup_files('generic');

% get all the trialFolders in directory
trialNames = {getfolders(sessionDir,'dynamic',1).name};

% directory of the scaled model
scaled_model_path = [sessionDir fp model_name];

% Run analysis for all the trials
iTrial = 1;

trialName = trialNames{iTrial};
trialPath = [sessionDir fp trialName];
trc_path  = [trialPath fp 'marker_experimental.trc'];

% Run all analysis
runIK(scaled_model_path,trialPath,IKsetup)
runID(scaled_model_path,trialPath,IDsetup)
runSO(scaled_model_path,trialPath,SOactuators)
runJRA(scaled_model_path,trialPath,JRLsetup)
