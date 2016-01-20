# TF2 fakeTube

TF2 fakeTube is an extremely barebones YouTube 2.0 API emulator to support the TF2 YouTube achievements.

**Use at your own risk!** I take no responsibility for what this does to you, your Steam account, your TF2 hat collection, or your neighbor's pet labradoodle. It seems quite safe to me, but it's up to you to decide whether you feel that this trick is okay to use on your own account.

## Introduction

This project exists to support users who want to "earn" the achievements in Team Fortress 2 related to replay uploads and views on YouTube. Since the YouTube APIs that TF2 used to upload and check view counts have been long since decommissioned by Google, it's impossible to earn these achievements naturally. Since Valve isn't maintaining the replay feature, (the official servers don't even record them any more), I figure they won't care if we jump through some hoops to satisfy our O.C.D. desires to have as many achievements as we can get.

Earn the rest naturally, of course. Achievement servers and cheats are lame. Except this one, which is awesome.

## Dependencies

- Python 2.7

## Building Your Replay

1. Play on a server that supports replays. You can filter by replay-capable servers in the main server list.
2. Play a bit and create a replay video.
3. Go into the replay editor and do some editing. Keep it short to cut down on render time. You can go all Martin Scorsese later.
4. Render the video to a .MOV file. This might take a bit.
5. When you get to the point where you've got a rendered file and TF2 says you can upload to YouTube, stop. That part no longer works.

## Faking the Upload

1. Go to `C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\replay\client\movies`, or wherever you've got Steam and TF2 installed.
2. Find the `.dmx` file that was just created for your shiny new rendered video. The first one will probably be named `movie_1000.dmx`.
3. Open the `.dmx` file in a text editor. You'll see something that looks like this:

		"movie_10000"
		{
			"handle"		"10000"
			"replay_handle"		"97"
			"rendered"		"1"
			"title"		"Explosive Action"
			"filename"		"20110527-224739-ctf_turbine_97_22_0.mov"
			"uploaded"		"0"
			"rendertime"		"2051.257080"
			"length"		"60.704998"
			"date"		"1178"
			"time"		"120087"
			"rendersettings"
			{
				"width"		"1920"
				"height"		"1080"
				"MotionBlurQuality"		"3"
				"fps.ups"		"24000"
				"fps.upf"		"1001"
				"codec"		"4"
				"encoding_quality"		"100"
				"mb_enabled"		"1"
				"aa_enabled"		"1"
				"raw"		"0"
			}
		}

4. Change the `"0"` next to `"uploaded"` to `"1"`.
5. Above the `"uploaded"` line, add this line:

		"upload_url"		"http://gdata.youtube.com/feeds/api/users/bubba/uploads/myAwesomeVideo?v=2"

6. Now the part you edited should look like below. If not, fix it.

		...
			"title"		"Explosive Action"
			"filename"		"20110527-224739-ctf_turbine_97_22_0.mov"
			"upload_url"		"http://gdata.youtube.com/feeds/api/users/bubba/uploads/myAwesomeVideo?v=2"
			"uploaded"		"1"
			"rendertime"		"2051.257080"
			"length"		"60.704998"
		...
		
7. Save and close the file.

Now we have a nice, fake URL for TF2 to find and check, but even if you had a video living at user "bubba" and with the ID "myAwesomeVideo", YouTube's 2.0 API is defunct and TF2 wouldn't be able to find it. That's where we need a fake web server running to answer TF2's queries.

## Running the Web Server

This step will create a web server running locally, but we will also need to tell TF2 that we'll be serving `gdata.youtube.com`, thank you very much.

1. Install Python 2.7
2. Run the included web server: `python server.py`
3. Check that Python says `Serving at port 80`. If so, the web server is running.
4. Open `C:\Windows\System32\drivers\etc\hosts` in your favorite text editor. Note that 32-bit text editors may not be able to see the `etc` directory inside `drivers`, so you might need to type that manually. That's because Windows is hiding 64-bit stuff from the 32-bit program.
5. Anyway, add this line to the bottom of the file:

		127.0.0.1 gdata.youtube.com
		
6. Save your `hosts` file. Make sure it didn't get saved as `hosts.txt`; that won't work.
	
This tells Windows that the specific YouTube server is actually hosted locally.

## Complete the Achievements

1. Run TF2
2. Click the "Replays" button
3. Click the thumbnail of the replay that you rendered earlier (and modified).

At this point, TF2 should immediately pop up all your new achievements. If not, check the lower right corner for stats related to your fake YouTube upload. If it says "not found", then something's not working.

## Cleanup

1. **Important!** When you're finished, don't forget to edit your `hosts` file and remove the `gdata.youtube.com` line you added.
2. You can kill the Python process by pressing `Ctrl-C`.

## Troubleshooting

- Once the web server is running and you've set up the `hosts` file change, open [this address](http://gdata.youtube.com/feeds/api/users/bubba/uploads/myAwesomeVideo?v=2) and see what you get. If you get a bunch of XML or a download named "myAwesomeVideo", your web server is working.
  - If you get an error that the page is not available, or `ERR_INVALID_RESPONSE`, then your `hosts` change may not be working.
- Try [this address](http://localhost/feeds/api/users/bubba/uploads/myAwesomeVideo?v=2) to directly connect without the `hosts` file.
  - If the above did not work, but this does, then something's wrong with your `hosts` file change.
- Check your Python instance to make sure it's still running. If Python starts and immediately goes away, it's not working. Try running it from a command prompt so you can check for errors.
- Check to make sure no other services are running on your computer with port :80 open. If that's the case, the Python server won't be able to use that port. I doubt TF2 will know how to work with other ports. I know I was unable to get it to connect directly to localhost, thus requiring the `hosts` change.