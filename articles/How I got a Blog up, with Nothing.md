A ~~complicated~~ simple guide to get a blog up for free*, while not using an SSG ([Static Site Generator](https://en.wikipedia.org/wiki/Static_site_generator)). A ~~reliable~~ working WordPress instance **to get things started**. Remember, life is like a sandbox, you can always fix things. ^ssg

%%for context: I started this website from my iPad alone.%%

## Prerequisites 

1. A resilient heart, because this *will* be a painful (but fun) process.
2. \*Preferably a good payment method (only *required* for the domain)(the domain is optional too)
3. An AI tool, or godly DuckDuckGo skills.

### Services to be Used

1. A Serverless provider like [Vercel](https://vercel.com) or [Netlify](https://netlify.com), *(both of which provide awesome free tiers to reel poor students in)*
2. A database cloud manager, like [TiDB Cloud](https://tidbcloud.com). Get your account ready before starting with the steps for reduced mental burden. Create an organisation. Clean up, your database will initially be called ‘test’ you can change that later.
3. An image hosting or cloud storage service, like [Cloudinary](https://cloudinary.com)
4. A source/git client like [GitHub](https://github.com).

## Steps to Making the Blog

1. Open Vercel, do the basic steps like creating a team etc. Then create a project, name it \<Your-Blog>. 
2. Filter through the templates available and find [ServerlessWP](https://serverlesswp.com/) (or alternatively, click on this hyperlink and hit deploy to Vercel)
3. Connect it to your Git Server and create a repository to host the source code for our website. Next, It’ll ask for your database details
4. Open TiDB Cloud. We’ll be connecting our cluster to Vercel. Click connect, then 
     - ‘Connect with’ Wordpress
     - Generate your password
     - Copy paste the details into vercel
     - Do not bother with the operating system. It has no effect on our workflow
![[database-creation.jpeg|300]]
5. **Ensure that your Vercel server and Database server are in the same region, or nearby.** Also ensure Fluid Compute is on.
    Note: To change your database region, you’ll need to recreate your cluster. Although TiDB by default, chooses the location which is close to you.
    *Additionally*, in case of failure, you may increase the max timeout duration to 300 seconds. All of these settings are in the ‘Functions’ tab.[^1]
![[vercel-timeout.jpeg]]
%% Pictorial guide to doing the above steps in vercel.%%
6. Now, let the deployment build, then head to the website through the domain provided by Vercel, ex: blog.vercel.app
7. Then create an account and it will take a minute to build.

## Troubleshooting 

If your Wordpress instance upon installing times out, **ensure** Step-5. 
Then, in TiDB, we’ll need to wipe out your whole database via the SQL Editor (or) alternatively, just deleting the cluster, remaking it and continuing from Step 4.
I’ll go with the SQL option.

### *Steps:*

1. Open your cluster page at [TiDB Cloud](https://tidbcloud.com) and from the menu at the top right, enter the SQL Editor.
2. Type in:
```
use test;
DROP DATABASE test;
CREATE DATABASE <the-name-you-want>;
```
%%
What it does is enter the database, then delete and create it again. We need to remove our old database because our instance failed to build properly.
%%
3. Then, hit ‘Run’.
4. Open your website again, and create again.

## Finishing Words

This guide is not conclusive, you *might* have to DuckDuckGo (I will not be using Google, fuck Google). But, I have tried my best to sprawl out all I know, because sometimes, you **need** a project in life yet can seem to find your way. Creating this blog meant a lot to me, it could to you too.

I’ll also be writing another article exploring the SSG [[#^ssg]] way too.

[^1]: The latency will be detrimental during the final install of Wordpress
