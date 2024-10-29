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

$thisprog = "ikonfriend.cgi";

$query = new CGI;

$inforum         = $query -> param('forum');
$intopic         = $query -> param('topic');
$action          = $query -> param('action');
$inrealname      = $query -> param('realname');
$intoname        = $query -> param('toname');
$infromemail     = $query -> param('fromemail');
$intoemail       = $query -> param('toemail');
$insubject       = $query -> param('subject');
$inemailmessage  = $query -> param('emailmessage');
$emailtopictitle = $query -> param('emailtopictitle');

$inrealname          = &cleaninput($inrealname);
$insubject           = &cleaninput($insubject);
$inemailmessage      = &cleaninput($inemailmessage);
$emailtopictitle     = &cleaninput($emailtopictitle);
$inforum             = &cleaninput($inforum);
$intopic             = &cleaninput($intopic);

$inmembername = cookie("amembernamecookie");
$inpassword   = cookie("apasswordcookie");

print header('text/html; charset=windows-1251');

if (($inforum) && ($inforum !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }


&title;


$output .= qq~
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
    <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
        <td valign=middle align=left><font face="$font" color=$fontcolormisc size=$dfontsize2>
        &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	    <br>
        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0902'}
        </td>
    </tr>
</table>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
        <td>
        <table cellpadding=6 cellspacing=1 border=0 width=100%>
        ~;



### Do we have email functions for this board?

if ($emailfunctions ne "on") { &error("$ibtxt{'0903'}&$ibtxt{'0904'}"); }



if ($action eq "send") {

    ### Check for blank fields and invalid email addresses
    $blankfields = "";
    if(!$inrealname)        { $blankfields = "yes"; }
    elsif(!$intoname)       { $blankfields = "yes"; }
    elsif(!$intoemail)      { $blankfields = "yes"; }
    elsif(!$infromemail)    { $blankfields = "yes"; }
    elsif(!$insubject)      { $blankfields = "yes"; }
    elsif(!$inemailmessage) { $blankfields = "yes"; }
    
    if ($blankfields) {
        &error("$ibtxt{'0903'}&$ibtxt{'0905'}");
        }
    
    if ($infromemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("$ibtxt{'0903'}&$ibtxt{'0906'}"); }
    if ($intoemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) { &error("$ibtxt{'0903'}&$ibtxt{'0906'}"); }
    
    ### If were still here, lets send the email
    
    $to = "$intoemail";
    $from = "$boardname <$infromemail>";
    $subject = "$insubject";

                
    $message .= "\n";
    $message .= "$boardname\n";
    $message .= "$boardurl/$forumsummaryprog\n";
    $message .= "$ibtxt{'0907'}\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inrealname $ibtxt{'0908'} $homename\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$inemailmessage\n\n";
    $message .= "$ibtxt{'0909'}: $emailtopictitle\n\n\n";
    $message .= "$boardurl/$threadprog?forum=$inforum&topic=$intopic\n";
    $message .= "---------------------------------------------------------------------\n\n";
    $message .= "$homename $ibtxt{'0910'}\n";
    $message .= "$ibtxt{'0911'}\n\n";
    $message .= "Ikonboard (c)2000 Ikonboard.com\n";
                

    &sendmail($from, $from, $to, $SMTP_SERVER, $subject, $message);

### Print message to user


            $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0912'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $ibtxt{'1004'}:
            <ul>
            <li><a href="$threadprog?forum=$inforum&topic=$intopic">$ibtxt{'0913'}</a>
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'0323'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;


} # end if action




else {

### Get Details

    $filetoopen = "$ikondir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
      flock FILE,2;
    @forums = <FILE>;
    close(FILE);

    foreach $forumline (@forums) { #start foreach @forums
        ($tempno, $trash) = split(/\|/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forumline);
            }
        }

    $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
      flock FILE,1;
    @allthreads = <FILE>;
    close(FILE);
    
    foreach $line (@allthreads) { #start foreach @threads
            ($tempno, $trash) = split(/\|/, $line);
            if ($intopic eq $tempno) {
                $linetokeep = $line;
            }
        } # end foreach
            
        
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$linetokeep);
        


### print form

    $topictitle = &cleanarea("$topictitle");

    $output .= qq~
    <form action="$boardurl/$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'0916'}</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize2>
    <b>Ikonfriend</b>: $ibtxt{'0917'} <a href="$threadprog?forum=$inforum&topic=$intopic">$topictitle</a> $ibtxt{'0918'}<br>
    $ibtxt{'0919'}
    <br>$ibtxt{'0920'}
    </td>
    <tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0921'}</b><br>$ibtxt{'0922'}</td>
    <td bgcolor=$miscbackone><input type=text size=40 name="realname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0923'}</b><br>$ibtxt{'0924'}</td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="fromemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0925'}</b><br>
    $ibtxt{'0926'}</td>
    <td bgcolor=$miscbackone><input type=text size=40 name="toname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0927'}</b><br>$ibtxt{'0928'}</td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="toemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0929'}</b><br>$ibtxt{'0930'}</td>
    <td bgcolor=$miscbackone><input type=text size=40 name="subject" value="$topictitle"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0931'}</b><br>$ibtxt{'0932'}</td>
    <td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">$ibtxt{'0933'}'$topictitle' $ibtxt{'0934'} '$homename'</textarea></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbackone align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="$ibtxt{'0041'}" name="Submit"></form></table></td></tr></table>
    ~;


} # end routine.


&output(
-Title   => $boardname, 
-ToPrint => $output, 
-Version => $versionnumber 
);

