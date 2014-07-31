phonebillspliter
================

This is a simple ATT Mobile Shared Plan bill spliter

PLEASE NOTE, I will not include the icon and gif file (required in the GUI) in the repo, one may replace with other icon and gif.


# This is a simple ATT Mobile Share Value Plan 10GB phone bill spliter.
# The basic pricing is as follows,
# 	Group owner basic is 104.54, including member basic and group addition
# 	Group member basic is 19.39
# So the average basic for each is 27.905, the average group addition per person is 8.515
# If there exists any over usage, will lead to extra fees, works as follows,
# 	Data over usage: fees applied to the owners, need to split with actual over-user
#   Other over usage & extra service: 
# 	  1) if applied to individual, counts on him/herself
# -->>2) if applied to owner, need calc manually (split method unkown)


#  Dev Plan
#  Based on currnt bill statements online, the bill split strategy is as above.
#  Bill details is available online in html format.
#  1. Input is from one html bill detail, and one pdf data usage detail;
#     html is auto-processed, pdf needs manually select and paste.
#  2. Calculation is done using above strategy;
#  3. Output is decided to be a text msg content.
# 
#  Future plan
#  Auto retreive and pre-process input html pdf, auto send bill text to members.
