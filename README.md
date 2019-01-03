# swxblock
The StepWise xBlock for the edX LMS platform

# HOW TO WORK DEV CYCLE
The edX documentation on setting up a dev environment with the xBlock SDK has two major missing steps. In section 3.2.3, you'll need to add these two commands at step 0 and 3.5: 

0. `mkdir var`
The var directory needs to exist or the manage.py commands will fail when they try to write to their log files which they expect to be in a var directory.

3.5 `make install`
After you run the `pip install -r requirements/base.txt` command, you need to run `make install` or the test page UI will crash with an error about `PluginMissingError: vertical_demo`

5. `pip install xblock-utils`
As far as I can tell, python doesnt have anything equivalent to JavaScript/NPM's package.json file which stores references to exteral libraries when you do an `npm install the_package` so that the next developer can simply run `npm install` and get them all loaded.  So we have to do it manually when setting up our xblock dev environment with this command.



# HOW TO INSTALL TO PRODUCTION
These instructions are based on [Lawrence McDaniel's](https://blog.lawrencemcdaniel.com/how-to-install-an-xblock/ "How to Install and xBlock") blog post.  For purposes of these instructions the xblock is called "swxblock".
1. Take a snapshot of your VM.  edX is fragile and you can easily blow stuff up.  If you are prompted at any time to upgrade anything, DON'T!!!  Your edX will invariably be permanently maimed and you'll have to restore from this snapshot.
2. Clone the xBlock's github repository to `/home/ubuntu` using `git clone git@github.com:QueriumCorp/swxblock.git`.  The repository reference can be copied from the GitHub repositories front page with `Clone or download > Clone with SSH`.  Note that the repository is private so the current user (probably root) needs to have a copy of the private key in ~/.ssh, that key needs to be `chmod 700 keyfile` and the corresponding public key has to be in your GitHub acct.
3. Make edxapp the owner and group of the xblock's files.
   * `sudo chown -R edxapp swxblock`
   * `sudo chgrp -R edxapp swxblock`
4. Install it.  Note that most web documentation says the command is `pip install -e .` but Lawrence says to use the following and it seems to work but you MUST use the -H or there will be errors.
   * `sudo -H -u edxapp /edx/bin/pip.edxapp install /home/ubuntu/swxblock`
5. Ensure a successful install. At the end of the output MUST be "Successfully" in green.  If you don't see successfully, it is likely there is debris left from a previous install.  See "HOW TO UPGRADE YOUR XBLOCK" and start from there.  If you don't see "Successfully" in green, you failed.
6. Compile the assets.  Note that the two paver processes take FOREVER.
   * `sudo -H -u edxapp bash`
   * `source /edx/app/edxapp/edxapp_env`
   * `cd /edx/app/edxapp/edx-platform`
   * `paver update_assets cms --settings=aws`
   * `paver update_assets lms --settings=aws`
7. Exit out of the edxapp_env.  Lawrence doesn't mention this but the next two commands won't work if you don't.
   * `exit`
8. Restart edx and its workers.  This takes several minutes to complete.  You can keep trying the site until it works. Don't forget the colons at the end of the line.  They matter.
   * `sudo /edx/bin/supervisorctl restart edxapp:`
   * `sudo /edx/bin/supervisorctl restart edxapp_worker:`
9. Enable the xBlock in your course. The xBlock should be in your edX instance, but the course owner must enable it for each course before it can be used in the course.  While in Studio, use `Settings > Advanced Settings`.  The first configuration property should be 'Advanced Module List'.  Why it says 'module' and not 'xBlock' is unknown but these 'modules' are 'xBlocks'.  This is a list or array and uses square brackets notation; aka "JSON" format.  So if there are no xBlocks enabled for this course the field should have an empty array (`[]`).  Enter your xBlock's name wrapped in double quotes (`[ "xblock" ]`).  Separate the xBlock names with commas like this (`[ "existing_xblock", "my_new_xblock" ]`).  You must check to make sure the quotes and commas are all correct as edX does no validation on that string.
10. Go to the unit in which you want to use your xBlock.  Click the green Advanced button with the flask icon and hopefully you'll see your xBlock.  If you don't, you're probably screwed and will have to start over.
# HOW TO UPGRADE YOUR XBLOCK
Just running the install process WILL NOT WORK!  You have to delete the old xblock from the server and then install it from scratch.
1. Verify the location of the installed xblock
   * `find / -type d -name "swxblock*"` which will return...
      * `/home/ubuntu/swxblock/swxblock/swxblock`
      * `/edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages/swxblock`
      * `/edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages/swxblock_xblock-0.1-py2.7.egg-info`
2. Delete the git clone's folder
   * `rm -Rf /home/ubuntu/swxblock`
3. Move to the site-packages folder
   * `cd /edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages`
4. Delete the `swxblock` and `swxblock...egg-info` directories and their contents
   * `rm -Rf /home/ubuntu/swxblock`
   * `rm -Rf /home/ubuntu/swxblock_xblock-0.1-py2.7.egg-info`
5. Check to make sure both directories are eliminated
   * `find . -name "swxblock*"` and ensure nothing is found.
6. Start the "HOW TO INSTALL TO PRODUCTION" instructions above
