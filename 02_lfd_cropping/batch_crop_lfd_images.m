addpath('../');
addpath('../utilities_matlab/');

global_variables;

%% Collect LFD images
lfd_rendering_filelist_fid = fopen(g_lfd_rendering_filelist);
line = fgetl(lfd_rendering_filelist_fid);
count = 0;
while ischar(line)
    count = count + 1;
    line = fgetl(lfd_rendering_filelist_fid);
end
fclose(lfd_rendering_filelist_fid);

image_filelist = cell(count, 1);
lfd_rendering_filelist_fid = fopen(g_lfd_rendering_filelist);
line = fgetl(lfd_rendering_filelist_fid);
count = 0;
while ischar(line)
    count = count + 1;
    image_filelist{count} = line;
    line = fgetl(lfd_rendering_filelist_fid);
end
fclose(lfd_rendering_filelist_fid);

local_cluster = parcluster('local');
poolobj = parpool('local', min(g_lfd_cropping_thread_num, local_cluster.NumWorkers));
fprintf('Batch cropping LFD images from \"%s\" to \"%s\" ...\n', g_lfd_rendering_folder, g_lfd_cropping_folder);
batch_crop(g_lfd_rendering_folder, g_lfd_cropping_folder, 0, image_filelist);
delete(poolobj);

exit;
