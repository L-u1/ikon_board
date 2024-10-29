#!/usr/bin/perl

#############################################################
# Ikonboard v2.1
# Copyright 2001 Ikonboard.com - All Rights Reserved
# Ikonboard is a trademark of Ikonboard.com
#
# Software Distributed by: Ikonboard.com
# Visit us online at http://www.ikonboard.com
# Email us on boards@ikonboard.com
#
# All files written by Matthew Mecham
#############################################################

use CGI::Carp "fatalsToBrowser";          # Output errors to browser
use CGI qw(:standard);                    # Saves loads of work
$CGI::POST_MAX=1024 * 150;                # limit post data
$CGI::DISABLE_UPLOADS = 1;                # Disable uploads

eval {
($0 =~ m,(.*)/[^/]+,)   and unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) and unshift (@INC, "$1");
require "ikon.lib";          # Require ikonboard ()
require "data/progs.cgi";    # Require prog names
require "data/boardinfo.cgi";# Require board info
require "data/styles.cgi";   # Require styles info
require "ikonmail.lib";      # Require email func ()
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                        # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "post.cgi";

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

for ('forum','topic','membername','password','action','postno','inshowsignature',
     'notify','inshowemoticons','previewfirst','intopictitle','intopicdescription',
     'inpost') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
    }



$inforum       = $forum;
$intopic       = $topic;
$inmembername  = $membername;
$inpassword    = $password;
$inpostno      = $postno;
$innotify      = $notify;
$currenttime   = time;
$postipaddress = $ENV{'REMOTE_ADDR'};


if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }

    if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }

    if ($inmembername eq "") {
        $inmembername = "$ibtxt{'0043'}";
        }
        else {
            &getmemberstime("$inmembername");
            }

    if ($action eq "addnew" or $action eq "addreply") {

    $namecookie = cookie(-name    =>   "amembernamecookie",
                         -value   =>   "$inmembername",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    $passcookie = cookie(-name    =>   "apasswordcookie",
                         -value   =>   "$inpassword",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
    print header(-cookie=>[$namecookie, $passcookie]);
    }
    else {
print header('text/html; charset=windows-1251');
        }

    if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("$ibtxt{'0901'}&$ibtxt{'0501'}"); }
    if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}"); }
    if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}"); }


    $helpurl = &helpfiles("Создание_Сообщений");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/help_b.gif" border=0></a>~;

    my %Mode = ( 
    'new'                 =>    \&newthread,
    'reply'               =>    \&reply,        
    'replyquote'          =>    \&replyquote
    );


    if($Mode{$action}) { 
        $Mode{$action}->();
        }
        elsif ($action eq "addnew"   && $previewfirst eq "no")  { &addnewthread; }
        elsif ($action eq "addnew"   && $previewfirst eq "yes") { &newthread; }
        elsif ($action eq "addreply" && $previewfirst eq "no")  { &addreply; }
        elsif ($action eq "addreply" && $previewfirst eq "yes") { &reply; }
        else { &error("$ibtxt{'0901'}&$ibtxt{'1401'}"); }


    &output(
    -Title   => "$boardname - $ibtxt{'1402'} $forumname", 
    -ToPrint => $output, 
    -Version => $versionnumber 
    );



############ New Thread side

sub newthread {

    

    ### Lets sort out the flood control

    &getmember("$inmembername");
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne "mo")) {
        $currenttime = time;
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("$ibtxt{'1403'}&$ibtxt{'1404'} $floodcontrollimit $ibtxt{'1405'}");
                }
            }

    &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
        
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   

    # Emoticons routine

    if ($emoticons eq "on") {
        $emoticonslink = qq~<a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">$ibtxt{'1408'}</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>$ibtxt{'1409'}<br>~;
        }


        
    # Add member to who's online    
        
    &whosonline("$inmembername|$ibtxt{'1410'} <a href=\"$forumsprog?forum=$inforum\">$forumname</a>|$ibtxt{'1602'}") if ($privateforum ne "yes");



    # Set up are we previewing/emailing/start thread allowance

    if ($previewfirst eq "yes") {
        &preview;
        $inpost =~ s/\<p\>/\n\n/g;
        $inpost =~ s/\<br\>/\n/g;
        }
        else {
            &mischeader("$ibtxt{'1403'}");
            }
        
    if ($emailfunctions eq "on") { 
           if ($innotify eq "yes") {
              $requestnotify = qq~<input type=checkbox name="notify" value="yes" checked>$ibtxt{'1411'}<br>~;
              } 
              else {
                   $requestnotify = qq~<input type=checkbox name="notify" value="yes">$ibtxt{'1411'}<br>~;
                   }
            }
        
    if ($startnewthreads eq "no") {
        $startthreads = "<b>$ibtxt{'1412'}</b>";
        }   
        else {
            $startthreads = "$ibtxt{'1413'}";
            }


    # Output the form

    
   &codebuttons;
    $output .= qq~
	$headcb
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
                <table cellpadding=4 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font face="$font" color=$titlefontcolor size=$dfontsize1><b>$ibtxt{'1452'}</b>: $startthreads</td>
                </tr>
                <tr><form action="$thisprog" method=post name=PostTopic>
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0909'}</b></font></td>
                <td bgcolor=$miscbackone valign=middle><input type=text size=40 maxlength=60 name="intopictitle" value="$intopictitle"></td>
                </tr><tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1416'}</b></font></td>
                <td bgcolor=$miscbackone valign=middle><input type=text size=40 maxlength=60 name="intopicdescription" value="$intopicdescription"></td>
                </tr><tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0727'}</b></font></td>
                <td bgcolor=$miscbackone valign=middle><input type=text size=20 name="membername" value="$inmembername"> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$registerprog">$ibtxt{'1417'}</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b></font></td>
                <td bgcolor=$miscbackone valign=middle><input type=password size=20 name="password" value="$inpassword"> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td>
                </tr><tr>
                <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1421'}</b><p>
                $ibtxt{'1422'} <b>$htmlstate</b> $ibtxt{'1423'}<p>$ibtxt{'1424'} <b>$idmbcodestate</b> $ibtxt{'1423'}<p>$emoticonslink</font></td>
                <td bgcolor=$miscbackone valign=middle>$bodycb<TEXTAREA cols=45 name=inpost rows=10 wrap=VIRTUAL>$inpost</TEXTAREA>$endcb</td>

                </tr><tr>
                <td bgcolor=$miscbacktwo valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1425'}</b><p>$helpurl</font></td>
                <td bgcolor=$miscbacktwo valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><input type=checkbox name="inshowsignature" value="yes" checked>$ibtxt{'1426'}<br>
                $requestnotify
                $emoticonsbutton
                <b>$ibtxt{'1427'}</b><input name="previewfirst" type="radio" value="yes"> $ibtxt{'0130'} &nbsp; <input name="previewfirst" type="radio" value="no" checked>$ibtxt{'0129'}</font>
                </font></td>
                </tr><tr>
                <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
                <input type=Submit value=$ibtxt{'0039'} name="Submit"  onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear">
                </form>
                </td></tr>
            </table>
        </tr></td></table>
        ~;

        

        } # end newthread routine








############### sub addnewthread #############

sub addnewthread { # start routine


    ### Lets sort out the flood control, incase they used the back button...

    &getmember("$inmembername");
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne "mo")) {
            $currenttime = time;
            ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
            $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("$ibtxt{'1403'}&$ibtxt{'1404'} $floodcontrollimit $ibtxt{'1405'}");
                }
            }
        
            
    # Sort out the forum moderator

    &moderator;

    if ($startnewthreads eq "no") {
        unless ($membercode eq "ad" || $inmembmod eq "yes") {
            &error("$ibtxt{'1428'}&$ibtxt{'1412'}");
            }
        }

    
    
    
    if    ($userregistered eq "no")     { &error("$ibtxt{'1428'}&$ibtxt{'1102'}"); }
    elsif ($inpassword ne $password)    { &error("$ibtxt{'1428'}&$ibtxt{'1430'}"); }
    elsif ($membercode eq "banned")     { &error("$ibtxt{'1432'}&$ibtxt{'1431'}"); }
    elsif ($intopictitle eq "")         { &error("$ibtxt{'1428'}&$ibtxt{'1433'}"); }
    elsif ($inpost eq "")               { &error("$ibtxt{'1428'}&$ibtxt{'1434'}"); }
    elsif ($intopictitle =~ /^\s/) { &error("Starting a thread&You must start the title with a letter or number"); }
    
    else  { # start else

        &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
        
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   

        
        ### Get a new thread number.

        $dirtoopen = "$ikondir" . "forum$inforum";
        opendir (DIR, "$dirtoopen"); 
        @dirdata = readdir(DIR);
        closedir (DIR);

        @sorteddirdata = grep(/thd/,@dirdata);
        @newdirdata = sort numerically(@sorteddirdata);
        @neworderdirdata = reverse(@newdirdata);

        $highest = @neworderdirdata[0];
        $highest =~ s/.thd//;
        $newthreadnumber = $highest + 1;

        # Open the bad word filter
        
        $filetoopen = "$ikondir" . "data/badwords.cgi";
        open (FILE, "$filetoopen");
        $badwords = <FILE>;
        close (FILE);
        
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                $inpost =~ s/$bad/$good/ig;
                $intopictitle =~ s/$bad/$good/ig;
                $intopicdescription =~ s/$bad/$good/ig;
                }
            }
        # Max char in word (intopictitle, intopicdescription)
        
        $intopictitle = Truncate ($intopictitle);
        $intopicdescription = Truncate ($intopicdescription);
        
        # Write the list.threadnumber entry 
        
        
        $filetoopen = "$ikondir" . "forum$inforum/$newthreadnumber.pl";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, ">$filetoopen");
          flock (FILE, 2);
        print FILE "$newthreadnumber|$intopictitle|$intopicdescription|open|0|0|$inmembername|$currenttime|$inmembername|$currenttime";
        close(FILE);

        # Create the new thread file
        
        $filetomake = "$ikondir" . "forum$inforum/$newthreadnumber.thd";
        $filetomake = &stripMETA($filetomake);
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$inmembername|$intopictitle|$postipaddress|$inshowemoticons|$inshowsignature|$currenttime|$inpost";
        close(FILE);

        
        # Update stats for member, and board
        
        $filetomake = "$ikondir" . "forum$inforum/lastpost.cgi"; 
		$filetomake = ($filetomake); 
		open(FILE, ">$filetomake"); 
		flock(FILE, 2); 
		print FILE "$inforum|$newthreadnumber|$intopictitle"; 
		close(FILE);
        
        &getforum("$inforum");        

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
        $numberofposts++;
        $lastpostdate = "$currenttime\%\%\%$threadprog?forum=$inforum&topic=$newthreadnumber\%\%\%$intopictitle" if ($privateforum ne "yes");
        chomp $lastpostdate;
        
        $filetomake = "$ikondir" . "members/$cleanmembername.cgi";
        $filetomake = &stripMETA($filetomake);
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$inmembername|$password|$membertitle|$membercode|$numberofposts|$emailaddress|$showemail|$ipaddress|$homepage|$aolname|$icqnumber|$location|$interests|$joineddate|$lastpostdate|$signature|$timedifference|$privateforums|$useravatar|$misc1|$misc2|$misc3";
        close(FILE);
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
          flock FILE, 1;
        @allforums = <FILE>;
        close(FILE);
        
        $filetomake = "$ikondir" . "data/allforums.cgi";
        $filetomake = &stripMETA($filetomake);
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $lastposter = $inmembername;
                    $lastposttime = $currenttime;
                    $threads = $newthreadnumber;
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;

        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        $filetomake = &stripMETA($filetomake);
        
        $totalthreads++;
        
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        
        
        # if the user wants email notifications, lets add them.
        
        if (($emailfunctions eq "on") && ($innotify eq "yes")) { # start mail
        
            $filetomake = "$ikondir" . "forum$inforum/$newthreadnumber.mal";
            
            open (FILE, ">$filetomake");
              flock (FILE, 2);
            print FILE "$inmembername|$emailaddress\n";
            close (FILE);
        
            } # end if
            
        
        $relocurl = "$threadprog?forum=$inforum&topic=$newthreadnumber";
        
        &mischeader("$ibtxt{'1440'}");
                    
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1441'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'0321'}
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$newthreadnumber">$ibtxt{'1443'}</a>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            
     rebuildLIST(-Forum=>"$inforum");

    } # end else

} # end addnewthread







###########################################
############## reply side #################

sub reply {

    


    ### Lets sort out the flood control

    &getmember("$inmembername");
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne "mo")) {
            $currenttime = time;
            ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
            $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("$ibtxt{''}&$ibtxt{'1404'} $floodcontrollimit $ibtxt{'1405'}");
                }
            }

    &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
        
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   

    if ($threadstate eq "closed" or $threadstate eq 'moved') { &error("$ibtxt{'1446'}&$ibtxt{'1447'}"); }


    if ($emoticons eq "on") {
        $emoticonslink = qq~<a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">$ibtxt{'1408'}</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>$ibtxt{'1409'}<br>~;
        }


    if ($emailfunctions eq "on") { 
           if ($innotify eq "yes") {
              $requestnotify = qq~<input type=checkbox name="notify" value="yes" checked>$ibtxt{'1411'}<br>~;
              } 
              else {
                   $requestnotify = qq~<input type=checkbox name="notify" value="yes">$ibtxt{'1411'}<br>~;
                   }
            }

    if ($previewfirst eq "yes") {
        &preview;
        $inpost =~ s/\<p\>/\n\n/g;
        $inpost =~ s/\<br\>/\n/g;
        }
        else {
            &mischeader("$ibtxt{'1446'}")
            }


    &codebuttons;
    $output .= qq~
	$headcb
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
            <table cellpadding=4 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font face="$font" color=$titlefontcolor size=$dfontsize1>$ibtxt{'1452'}: $topictitle</td>
                </tr>
                <tr><form action="$thisprog" method=post name=PostTopic>
                    <input type=hidden name="action" value="addreply">
                    <input type=hidden name="forum" value="$inforum">
                    <input type=hidden name="topic" value="$intopic">
                </tr><tr>
                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0727'}</b></font></td>
                    <td bgcolor=$miscbackone valign=middle><input type=text size=20 name="membername" value="$inmembername"><font face="$font" color=$fontcolormisc size=$dfontsize1> &nbsp; <a href="$registerprog">$ibtxt{'1417'}</a></font></td>
                </tr><tr>
                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b></font></td>
                    <td bgcolor=$miscbackone valign=middle><input type=password size=20 name="password" value="$inpassword"><font face="$font" color=$fontcolormisc size=$dfontsize1> &nbsp; <a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td>
                </tr><tr>
                    <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1421'}</b><p>
                    $ibtxt{'1422'} <b>$htmlstate</b> $ibtxt{'1423'}<p>$ibtxt{'1424'} <b>$idmbcodestate</b> $ibtxt{'1423'}<p>$emoticonslink</font></td>
                    <td bgcolor=$miscbackone valign=middle>$bodycb<TEXTAREA cols=45 name=inpost rows=10 wrap=VIRTUAL>$inpost</TEXTAREA>$endcb</td>
                </tr><tr>
                    <td bgcolor=$miscbacktwo valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1425'}</b><p>$helpurl</font></td>
                    <td bgcolor=$miscbacktwo valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><input type=checkbox name="inshowsignature" value="yes" checked>$ibtxt{'1426'}<br>
                    $requestnotify
                    $emoticonsbutton
                    <b>$ibtxt{'1427'}</b><input name="previewfirst" type="radio" value="yes"> $ibtxt{'0130'} &nbsp; <input name="previewfirst" type="radio" value="no" checked> $ibtxt{'0129'}</font>
                    </font></td>
                </tr><tr>
                    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
                    <input type=Submit value=$ibtxt{'0039'} name="Submit" onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear"></form>
                </td></tr>
            </table></tr></td>
        </table>
        ~;
        
        
        # Lets display the thread review

        $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
          flock(FILE, 2);
        @threads = <FILE>;
        close(FILE);

        @sortedthreads = reverse(@threads);

        &threadreview;
    
    } # end add reply routine




##### Reply with quote

sub replyquote {

    


    ### Lets sort out the flood control

    &getmember("$inmembername");
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne "mo")) {
            $currenttime = time;
            ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
            $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("$ibtxt{'1446'}&$ibtxt{'1404'} $floodcontrollimit $ibtxt{'1405'}");
                }
            }
    &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
   
        if ($threadstate eq "closed") { &error("$ibtxt{'1446'}&$ibtxt{'1447'}"); }     

        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   

    # Get the post to edit

    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, $filetoopen);
      flock(FILE, 1);
    @threads = <FILE>;
    close(FILE);

    $posttoget = $inpostno;
    $posttoget--;

    ($membername1, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\|/, @threads[$posttoget]);
        
    $post =~ s/\<p\>/\n\n/g;
    $post =~ s/\<br\>/\n/g;
    
    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);   
    $postdate = &dateformat("$postdate");




### Print form



    $rawpost = $post;

    if ($previewfirst eq "yes") {
        $rawpost = $inpost;
        $rawpost =~ s/\<p\>/\n\n/g;
        $rawpost =~ s/\<br\>/\n/g;
        &preview;
        }
        else {
            &mischeader("$ibtxt{'1444'}");
            }


    if ($threadstate eq "closed") { &error("$ibtxt{'1446'}&$ibtxt{'1447'}"); }

    if ($emoticons eq "on") {
        $emoticonslink = qq~<a href="javascript:openScript('$miscprog?action=showsmilies',300,350)">$ibtxt{'1408'}</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>$ibtxt{'1409'}<br>~;
        }
    
    if ($emailfunctions eq "on") { $requestnotify = qq~<input type=checkbox name="notify" value="yes">$ibtxt{'1411'}<br>~; }


    $temppost = qq~\[quote\]Quote: from $membername1 on $postdate\[br\]$rawpost\[\/quote\]~;

    &codebuttons;
    $output .= qq~
	$headcb
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
                <table cellpadding=4 cellspacing=1 border=0 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2><font face="$font" color=$titlefontcolor size=1>$ibtxt{'1452'}: $topictitle</td>
                </tr>
                <tr><form action="$thisprog" method=post name=PostTopic>
                    <input type=hidden name="action" value="addreply">
                    <input type=hidden name="forum" value="$inforum">
                    <input type=hidden name="topic" value="$intopic">
                </tr><tr>
                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0727'}</b></font></td>
                    <td bgcolor=$miscbackone valign=middle><input type=text size=20 name="membername" value="$inmembername"><font face="$font" color=$fontcolormisc size=$dfontsize1> &nbsp; <a href="$registerprog">$ibtxt{'1417'}</a></font></td>
                </tr><tr>
                    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0728'}</b></font></td>
                    <td bgcolor=$miscbackone valign=middle><input type=password size=20 name="password" value="$inpassword"><font face="$font" color=$fontcolormisc size=$dfontsize1> &nbsp; <a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td>
                </tr><tr>
                    <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1421'}</b><p>
                    $ibtxt{'1422'} <b>$htmlstate</b> $ibtxt{'1423'}<p>$ibtxt{'1424'} <b>$idmbcodestate</b> $ibtxt{'1423'}<p>$emoticonslink</font></td>
                   <td bgcolor=$miscbackone valign=middle>$bodycb<TEXTAREA cols=45 name=inpost rows=10 wrap=VIRTUAL>$temppost</TEXTAREA>$endcb</td>
                </tr><tr>
                    <td bgcolor=$miscbacktwo valign=top><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1425'}</b></font></td>
                    <td bgcolor=$miscbacktwo valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><input type=checkbox name="inshowsignature" value="yes" checked>$ibtxt{'1426'}<br>
                    $requestnotify
                    $emoticonsbutton
                    <b>$ibtxt{'1427'}</b><input name="previewfirst" type="radio" value="yes"> $ibtxt{'0130'} &nbsp; <input name="previewfirst" type="radio" value="no" checked> $ibtxt{'0129'}</font>
                    </font></td>
                </tr><tr>
                    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
                    <input type=Submit value=$ibtxt{'0039'} name="Submit" onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear"></form>
                    </td></tr></table></tr></td></table>
                    ~;



    # Print the thread summary
    

    @sortedthreads = reverse(@threads);

    &threadreview;

} # end add reply quote









##### add the replyto the file.

sub addreply { # start routine


    ### Lets sort out the flood control, incase they used the back button...

    &getmember("$inmembername");
        if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne "mo")) {
            $currenttime = time;
            ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
            $lastpost = ($lastpost + $floodcontrollimit);
            if ($lastpost > $currenttime)  {
                &error("$ibtxt{'1446'}&$ibtxt{'1404'} $floodcontrollimit $ibtxt{'1405'}");
                }
            }

    
    if ($userregistered eq "no")     { &error("$ibtxt{'1432'}&$ibtxt{'1102'}"); }
    elsif ($inpassword ne $password) { &error("$ibtxt{'1432'}&$ibtxt{'1430'}"); }
    elsif ($membercode eq "banned")  { &error("$ibtxt{'1432'}&$ibtxt{'1431'}"); }
    elsif ($inpost eq "")            { &error("$ibtxt{'1428'}&$ibtxt{'1434'}"); }

    else { # start else

        &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }

        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   
 
        # Grab the thread file
        
        $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen");
        @allmessages = <FILE>;
        close(FILE);

        $totalthreadposts = @allmessages;
        
        ($trash, $topictitle) = split(/\|/,$allmessages[0]);

        # Open the bad word filter
        
        $filetoopen = "$ikondir" . "data/badwords.cgi";
        open (FILE, "$filetoopen");
        $badwords = <FILE>;
        close (FILE);
    
        if ($badwords) {
            @pairs = split(/\&/,$badwords);
            foreach (@pairs) {
                ($bad, $good) = split(/=/,$_);
                $inpost =~ s/$bad/$good/ig;
                $intopictitle =~ s/$bad/$good/ig;
                $intopicdescription =~ s/$bad/$good/ig;
                }
            }
    
        my $file = "$ikondir" . "forum$inforum/$intopic.pl";
        open (ENT, $file);
          flock ENT, 1;
        $in = <ENT>;
        close (ENT);
        
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$in);
        if ($threadstate eq "closed" or $threadstate eq 'moved') { &error("$ibtxt{'1446'}&$ibtxt{'1447'}"); }

        require "$ikondir" . "data/boardstats.cgi";

###########################################################################
# Склеивание постов


        $num = $totalthreadposts-1;
        ($inmembername_OLD, $topictitle_OLD, $postipaddress_OLD, $inshowemoticons_OLD, $inshowsignature_OLD, $currenttime_OLD, $inpost_OLD) = split (/\|/, $allmessages[$num]);
        chomp ($inpost_OLD);


        # Эти две строки отвечают за склеивание постов если новый пост не позднее 2х часов
        # Если хотите уменьшить время замените число 7200 на другое.
        # Если вы хотите отключить эту возможность закоментируйте две строки, и раскоментируйте третью 
               
        $timelimit = $currenttime - $currenttime_OLD;
        if ($inmembername_OLD eq $inmembername && $timelimit < 7200 && (!($inmembername eq "$ibtxt{'0043'}" && $inmembername_OLD eq "$ibtxt{'0043'}" && $postipaddress_OLD ne $postipaddress))) {
        #if ($inmembername_OLD eq $inmembername) {
        
        
        my $current_time = $currenttime + ($timedifferencevalue*3600) + ($timezone*3600);
        my $current_time = &dateformat("$currenttime");
        
        my $addon = "<p><br>[s][b]\($ibtxt{'9989'}  $current_time.\)[/b][/s]<p><br>";
        
      
        $inpost_OLD = $inpost_OLD . $addon . "$inpost\n";
        
        $currenttime = $currenttime_OLD;
        
        $postcountcheck = 0;
        foreach $postline (@allmessages) {
            chomp $postline;
                if ($postcountcheck eq $num) {
                    $processed_data .= "$inmembername_OLD|$topictitle_OLD|$postipaddress_OLD|$inshowemoticons_OLD|$inshowsignature_OLD|$currenttime_OLD|$inpost_OLD";
                }
                else { $processed_data .= "$postline\n"; }
                $postcountcheck++;
                }
            $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
            open(FILE, ">$filetoopen");
             flock(FILE, 2);
            print FILE $processed_data;
            close(FILE);
            undef $processed_data;
          
             
         
        } else {
                
        $filetomake = "$ikondir" . "forum$inforum/$intopic.thd";
        $filetomake = &stripMETA($filetomake);
        foreach $messages (@allmessages) {
            chomp $messages;
            $processed_data .= "$messages\n";
            }
        $processed_data .= "$inmembername|$topictitle|$postipaddress|$inshowemoticons|$inshowsignature|$currenttime|$inpost";
        open(FILE, ">$filetomake");
         flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;
        
        $filetomake = "$ikondir" . "forum$inforum/lastpost.cgi"; 
   		$filetomake = ($filetomake); 
		open(FILE, ">$filetomake"); 
		flock(FILE, 2); 
		print FILE "$inforum|$intopic|$topictitle"; 
		close(FILE); 
        
        $numberofposts++; # плюс счетчик сюда впихиваем.
        $totalposts++;
        $addpost_ = 1;  
        }



####################################################################        



#$filetomake = "$ikondir" . "forum$inforum/$intopic.thd";
#        $filetomake = &stripMETA($filetomake);
#        foreach $messages (@allmessages) {
#            chomp $messages;
#            $processed_data .= "$messages\n";
#            }
#        $processed_data .= "$inmembername|$topictitle|$postipaddress|$inshowemoticons|$inshowsignature|$currenttime|$inpost";
#        open(FILE, ">$filetomake");
#          flock(FILE, 2);
#        print FILE $processed_data;
#        close(FILE);
#        undef $processed_data;
        
        $threadposts = @allmessages;
        
        open(FILE, ">$file");
          flock(FILE, 2);
        print FILE "$intopic|$topictitle|$topicdescription|$threadstate|$threadposts|$threadviews|$startedby|$startedpostdate|$inmembername|$currenttime";
        close(FILE);

            
        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
        #$numberofposts++;
        $lastpostdate = "$currenttime\%\%\%$threadprog?forum=$inforum&topic=$intopic\%\%\%$topictitle" if ($privateforum ne "yes");
        chomp $lastpostdate;
        
        $filetomake = "$ikondir" . "members/$cleanmembername.cgi";
        $filetomake = &stripMETA($filetomake);
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "$inmembername|$password|$membertitle|$membercode|$numberofposts|$emailaddress|$showemail|$ipaddress|$homepage|$aolname|$icqnumber|$location|$interests|$joineddate|$lastpostdate|$signature|$timedifference|$privateforums|$useravatar|$misc1|$misc2|$misc3";
        close(FILE);

        $filetoopen = "$ikondir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, $filetoopen);
          flock (FILE, 1);
        @allforums = <FILE>;
        close(FILE);
  
$filetomake = "$ikondir" . "data/allforums.cgi";
        $filetomake = &stripMETA($filetomake);
        foreach $forum (@allforums) { #start foreach @forums
        chomp($forum);
            ($tempno, $trash) = split(/\|/,$forum);
                if ($inforum eq $tempno) {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
                    $lastposter = $inmembername;
                    $lastposttime = $currenttime;
                    if ($addpost_) {$posts++;}
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;



        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        $filetomake = &stripMETA($filetomake);
        

        
        open(FILE, ">$filetomake");
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);
        
    ### email functions
        
            # First, lets open the maildata file, and add (if needed) the new requestee.
        
        if ($emailfunctions eq "on") { # start mail
        
            
            $filetoopen = "$ikondir" . "forum$inforum/$intopic.mal";
            open (FILE, "$filetoopen");
            @maildata = <FILE>;
            close (FILE);
        
            
            if ($innotify eq "yes") {
                open (FILE, ">$filetoopen");
                  flock (FILE, 2);
                print FILE "$inmembername|$emailaddress\n";
                foreach $line (@maildata) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                close (FILE);
                }
        
            # Lets sort the data (there's no point adding the new requestee at this point!)
        
            foreach $dataline (@maildata) {
                ($postersname,$posteremailaddress) = split(/\|/,$dataline);
                
                if ($lastemailsent ne $postersname) {
                
                # No point in getting your own post emailed to you, so...
                
                    if ($inmembername eq $postersname) { next; }
                
                    # If not,carry on!
                    
                        $output .= "\n\n<!-- Processing Emails --> \n\n";

                        $toemail = $posteremailaddress;
                        chomp $toemail;
                        $toemail =~ s/\\//g;
                        $fromemail = $adminemail_out;
                        chomp $fromemail;
                        $fromemail =~ s/\\//g;

                        $topictitle =~ s/&quot;/\"/g;
                        $topicdescription =~ s/&quot;/\"/g;
                        
                        $to = $toemail;
                        $from = "$boardname <$fromemail>";
                        $subject = "[$forumname] $ibtxt{'1453'}";

                        $message .= "\n";
                        $message .= "$boardtitle\n";
                        $message .= "$boardurl/$forumsummaryprog\n";
                        $message .= "---------------------------------------------------------------------\n\n";
                        $message .= "$postersname, $inmembername $ibtxt{'1454'}\n\n";
                        $message .= "$ibtxt{'1455'} $category\n";
                        $message .= "$ibtxt{'1456'} $forumname\n";
                        $message .= "$ibtxt{'1457'} $topictitle\n";
                        $message .= "$ibtxt{'1458'} $topicdescription\n\n";
                        $message .= "$ibtxt{'1459'}\n\n";
                        $message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n\n";
                        $message .= "---------------------------------------------------------------------\n";
                        
                        &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message );
                    
                        $lastemailsent = "$postersname";
                    
                    # trash the details, just to be safe.
                    
                    $message = "";
                    $to = "";
                    $from = "";
                    $subject = "";
                  
                  } # end if       
                
                } # end foreach
             
             } # end email send.


        $numberofitems = $threadposts + 1;
        $numberofpages = $numberofitems / $maxthreads;

        if ($numberofitems > $maxthreads) { #if
            if ($maxthreads < $numberofitems) { #2
                ($integer,$decimal) = split(/\./,$numberofpages);
                    if ($decimal > 0) { $numberofpages = $integer + 1; }
                        $pagestart = 0;
                        $counter = 0;
                        while ($numberofpages > $counter) { #3
                            $counter++;
                            $threadpages .= qq~<a href="$threadprog?forum=$inforum&topic=$topicid&start=$pagestart"> $counter </a>~;
                            $pagestart = $pagestart + $maxthreads;
                            } #e3
                        } #e2
                    $pagestoshow = qq~<font face="$font" color=$forumfontcolor size=$dfontsize1> &nbsp;[ $ibtxt{'0605'}&nbsp;$threadpages ]~;
                    } #1


        
        &mischeader("$ibtxt{'1461'}");
        my $gotopage = ($pagestart - $maxthreads);
           $gotopage = 0 unless $gotopage > 0;
        $relocurl = "$threadprog?forum=$inforum&topic=$intopic&start=$gotopage";
        
                    
        $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'1462'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'0321'}
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic&start=$gotopage">$ibtxt{'0913'}</a> $pagestoshow
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;
            

      rebuildLIST(-Forum=>"$inforum");      


    } # end else
    

} # end addreply



###########################
# Thread Review

sub threadreview {

    $output .= qq~
        <p>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr><td>
        <table cellpadding=8 cellspacing=1 border=0 width=100%>
        <tr>
        <td bgcolor=$titlecolor colspan=2><font face="$font" color=$titlefontcolor size=$dfontsize2><b>$ibtxt{'1467'} $topictitle ($ibtxt{'1468'})</b></td>
        ~;

    $reviewcount=1;
    foreach $threadline (@sortedthreads) {
    unless($reviewcount > 20) {
    
        ($membername, $topictitle, $postipaddress ,$showemoticons ,$showsignature ,$postdate ,$post) = split(/\|/, $threadline);
        $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $postdate = &dateformat("$postdate");

        $post = &ikoncode("$post");
        $post = &doemoticons("$post");
        $post =~ s/\:\)/<img src=\"$imagesurl\/emoticons\/smile.gif\" border=\"0\">/g;
        $post =~ s/\;\)/<img src=\"$imagesurl\/emoticons\/wink.gif\" border=\"0\">/g;
        $post =~ s/\:\(/<img src=\"$imagesurl\/emoticons\/sad.gif\" border=\"0\">/g;
        $post =~ s/\:\o/<img src=\"$imagesurl\/emoticons\/shocked.gif\" border=\"0\">/g;
        


    $output .= qq~
        <tr>
            <td bgcolor="$miscbackone" rowspan=2 valign="top" width=20%><font face="$font" color=$fontcolormisc size=$dfontsize2>
            <b>$membername</b></font></td>
            <td bgcolor="$miscbackone"><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0319'} $postdate</b></td>
        </tr>
        <tr>
            <td bgcolor="$miscbackone"><font face="$font" color=$fontcolormisc size=$dfontsize2>$post</td>
        </tr>
        <tr>
            <td colspan=2 bgcolor="$miscbacktwo">&nbsp;</td>
        </tr>
        ~;
	$reviewcount++;
	}
        } # end foreach
    $output .= qq~</table></td></tr></table>~;
} # end routine
   
