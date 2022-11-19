# WEEKLY REPORT 3

I feel like I've spent more time planning/reading/procrastinating/trial-and-erroring than actually coding this week. Dunno why it seems so difficult to Create Something. Like, this feels way beyond my skills and knowledge.

Idk, I suppose this is some sort of a mental block thing, as I'm constantly doubting myself (and my skills), thus not willing to *start* writing anything. When I get started, I'm more than happy to sit at my desk for 8+ hours, getting things done, so I have to figure out how to motivate myself to, well, begin. 

## Project progress

It has been a slow start – more time has been used to do research than writing code. The first issue, although simple at heart, took me ages to overcome: if I'm making a JPEG converter, what is (/are) the file format(/s) I am converting *from*?

So, as a photographer, I mainly work with RAW images (namely, CR2). RAW images tend to be camera or software specific, and who wants to convert those into JPEGs anyway? JPEG being a raster graphic, there would be no point considering vector graphics, really, so that already excludes several formats. TIFF is a nice lossless format I tend to use for the high-quality prints anyway, and also widely used for raster graphics. Thus, I will focus on TIFF to JPEG conversions here.

Secondly, the RBG to YCbCr conversion took way more time than I thought. My linear algebra is rusty, so matrix revision was needed, as well as time for understanding the conversion formulas. Furthermore, halfway through figuring it out it struck me that having a image object class would make more sense than just separate functions, so yay refactoring!

Docstring & Pylint (& codetags) are in use, so everything should be readable.

## This week I learnt...

Not the main focus of this course/project, but getting more familiar with NumPy has been the Number One achievement this week. Linear algebra revision has been good, too, I suppose. Even if it on paper it looks like the project has not moved forwards a lot, I've gone through half a notebook (not really, but feels like it) trying to figure out the maths for the next steps.

## Questions, problems, and such
Is it enough to convert only RGB to YCbCr, or do I need to figure out how to convert true grayscale images too? I mean, it would be interesting to see the difference in compression between the two.

As for the demo on exam week(?), any possibilities to participate remotely? If not, would be good to get at least the date asap, as I live abroad and need to book flights if I gotta be in Helsinki...

## What next?

So, at this point, we have a working RGB to YCbCr to RGB converter (tested manually) – not a lot, I am aware of this. Automated tests for that will hopefully be written before this weeks deadline. The plan for next week is to tackle subsampling and splitting the raw data into Minimum Coded Unit (MCU) blocks. 
