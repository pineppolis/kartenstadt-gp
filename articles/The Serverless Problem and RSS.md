#### Tldr; RSS: https://kartenstadt/feed

If you’ve read the previous articles, you might know that this website runs on a [Serverless Wordpress](https://serverlesswp.com) instance. Any Serverless setup will have one thing in common, a read-only file system. Which will be the cause of my problems for a while.

# The Problem

My **media** won’t load on an RSS Reader, and is tedious while publishing too.

I mentioned the file system being read-only, so, where am I storing my text files and **media** files then?
The creator of this system is quite ingenious, all of my text files are never really stored on server, they stay on the **Database.**

### What is a [database](https://developer.mozilla.org/en-US/docs/Glossary/Database)?
It is where you store data that you need actively and it indexes them such that it can be searched easily. A database is basically a table, that’s what it is.

### So what’s the problem?
*MEDIA.* (imagine it like the [Sega intro](https://youtu.be/GpzH0WJ52kc?si=ERJo2QEDQPmMH4Kb)) You can’t store media in a table unless you are a crazy math nerd (I bet you can find it on Youtube). I was using [Cloudinary](https://cloudinary.com) before tackling the issue of an RSS reader, which is supported by default in every Wordpress website, mine supports it too.

Thus, I tested it, the text rendered just fine, the problem was the *MEDIA*. It did not work, and there are two fixes:
1. I switch away from a Serverless setup. (or)
2. I buy into a cloud object storage system.
3. Third option does exist btw, just not to the standards I wish to hold this website to.
And, currently, I like **none** of these.

### What’s Object Storage?
You might ask. I don’t know, but I did DuckDuckGo it.
It’s storage, it’s just normal storage without labels like the database. You need the exact address to refer to your file.Like the file system on your pc.
However, object storage extend beyond this definition. They have this thing called a [CDN (Content Delivery Network)](https://developer.mozilla.org/en-US/docs/Glossary/CDN)

### What’s a CDN?
I attached an MDN(Mozilla Docs) link above, but here’s a quick summary. They take your file, spread it across the entire globe (ie. their servers) and then distribute it accordingly. When a user in Asia connects to your website, they get the Asia server.
However, I don’t give a shit. This will have me lose control over the files and I’m a privacy freak who still has a gmail address.

## My Solution

I will be ditching media *for now*, including the old uploaded files. I want RSS to work and my website to be reliable.

# RSS

Why do i even want RSS? It’s simple, it debloats my website and gives you the content right away (not to say that my site is bloated, its quite appealing). And It’ll help with my original goal of keeping this website available everywhere easily.

My suggested aggregators:
- For all Apple: [NetNewsWire](https://apps.apple.com/in/app/netnewswire-rss-reader/id1480640210)
- For Android: [ReadYou](https://f-droid.org/packages/me.ash.reader/)
- For Linux & Windows: [Akregator](https://apps.kde.org/en-gb/akregator/)

You can add my feed manually in the apps via the URL: https://kartenstadt.org/feed.
I’ll also be adding a button on the home page.

PS: I *always* attach a reliable source. Like for database and CDN, not because I’m stupid and can’t read, there are just better ways to get into this stuff, and the [MDN](https://developer.mozilla.org/en-US/) website is so beautiful.
In case you have a better source or would like to tell me something really really really cool (or lame), I have an email: pineppolis@kartenstadt.org

11-02-2026
