# swxblock
The StepWise xBlock for the edX LMS platform

# HOW TO BUILD
More to come

# HOW TO INSTALL
These instructions are based on [Lawrence McDaniel's](https://blog.lawrencemcdaniel.com/how-to-install-an-xblock/ "How to Install and xBlock") blog post.  For purposes of these instructions the xblock is called "xblock".
1. Take a snapshot of your VM.  edX is fragile and you can easily blow stuff up.  If you are prompted at any time to upgrade anything, DON'T!!!  Your edX will invariably be permanently maimed and you'll have to restore from this snapshot.
2. Clone the xBlock's github repository to `/home/ubuntu` using `git clone git@github.com:QueriumCorp/xblock.git`.  The repository reference can be copied from the GitHub repositories front page with `Clone or download > Clone with SSH`.  Note that the repository is private so the current user (probably root) needs to have a copy of the private key in ~/.ssh, that key needs to be `chmod 700 keyfile` and the corresponding public key has to be in your GitHub acct.
3. Make edxapp the owner and group of the xblock's files.
   * `sudo chown -R edxapp xblock`
   * `sudo chgrp -R edxapp xblock`
4. Install it.  Note that most web documentation says the command is `pip install -e .` but Lawrence says to use the following and it seems to work but you MUST use the -H or there will be errors.
   * `sudo -H -u edxapp /edx/bin/pip.edxapp install /home/ubuntu/xblock`
5. Compile the assets.  Note that the two paver processes take FOREVER.
   * `sudo -H -u edxapp bash`
   * `source /edx/app/edxapp/edxapp_env`
   * `cd /edx/app/edxapp/edx-platform`
   * `paver update_assets cms --settings=aws`
   * `paver update_assets lms --settings=aws`
6. Exit out of the edxapp_env.  Lawrence doesn't mention this but the next two commands won't work if you don't.
   * `exit`
7. Restart edx and its workers.  This takes several minutes to complete.  You can keep trying the site until it works. Don't forget the colons at the end of the line.  They matter.
   * `sudo /edx/bin/supervisorctl restart edxapp:`
   * `sudo /edx/bin/supervisorctl restart edxapp_worker:`
8. Enable the xBlock in your course. The xBlock should be in your edX instance, but the course owner must enable it for each course before it can be used in the course.  While in Studio, use `Settings > Advanced Settings`.  The first configuration property should be 'Advanced Module List'.  Why it says 'module' and not 'xBlock' is unknown but these 'modules' are 'xBlocks'.  This is a list or array and uses square brackets notation; aka "JSON" format.  So if there are no xBlocks enabled for this course the field should have an empty array (`[]`).  Enter your xBlock's name wrapped in double quotes (`[ "xblock" ]`).  Separate the xBlock names with commas like this (`[ "existing_xblock", "my_new_xblock" ]`).  You must check to make sure the quotes and commas are all correct as edX does no validation on that string.
9. Go to the unit in which you want to use your xBlock.  Click the green Advanced button with the flask icon and hopefully you'll see your xBlock.  If you don't, you're probably screwed and will have to start over.
# HOW TO UPGRADE YOUR XBLOCK
No idea.  Re-running the install process has not had any effect so far.