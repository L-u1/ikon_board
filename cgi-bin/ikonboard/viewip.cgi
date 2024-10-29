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
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                     # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "viewip.cgi";

$query = new CGI;
	
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$checked        = $query -> param('checked');
$inpostno       = $query -> param('postno');
$inmembername   = $query -> param('membername');
$inpassword     = $query -> param('password');
$inmembername   = &cleaninput("$inmembername");
$inpassword     = &cleaninput("$inpassword");

print header('text/html; charset=windows-1251');

if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }

if ($inmembername eq "") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        }

    &title;

    $filetoopen = "$ikondir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    @forums = <FILE>;
    close(FILE);

    foreach $forumline (@forums) { #start foreach @forums
        ($tempno, $trash) = split(/\|/,$forumline);
        if ($inforum eq $tempno) {
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forumline);
            }
        }

### Forum Graphic Stuff


    if ($forumgraphic) {
        $forumgraphic = qq~<a href="$forumsprog?forum=$inforum"><img src="$forumgraphic" border=0></a>~;
        }


### Grab the post to edit

    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
    open(FILE, "$filetoopen");
    @threads = <FILE>;
    close(FILE);

    $posttoget = $inpostno;
    $posttoget--;

    ($postmembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\|/,@threads[$posttoget]);
    
    $postdate = $postdate + ($timezone*3600) + ($timedifferencevalue*3600);
    $postdate = &dateformat("$postdate");
    
    ($trash, $topictitle) = split(/\|/,@threads[0]);

### Print the header


    $output .= qq~
    
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
                <font face="$font" color=$fontcolormisc size=$dfontsize2>
	            &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	            <br>
                &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsprog?forum=$inforum">$forumname</a>
                <br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'2401'}<a href="$threadprog?forum=$inforum&topic=$intopic">$topictitle</a>
            </td>
        </tr>
    </table>
    <p>

    ~;


### Check for authorisation.

    
    &getmember("$inmembername");
    &moderator;

    $cleartoedit = "no";
    if ($userregistered eq "no") { &error("$ibtxt{'2413'}"); }
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartomove = "yes"; }
    unless ($cleartomove eq "yes") { $cleartomove = "no"; }
    
        if ($cleartomove eq "no" && $checked eq "yes") { &error("$ibtxt{'2402'}&$ibtxt{'0504'}"); }    
        
        if (($cleartomove eq "yes") && ($checked eq "yes")) {
        




### Get the IPaddress when the user signed up       


            $nametocheck = $postmembername;
            $nametocheck =~ s/ /\_/g;
            $filetoopen = "$ikondir" . "members/$nametocheck.cgi";
            open(FILE,"$filetoopen");
            $filedata = <FILE>;
            close(FILE);
            chomp($filedata);
            ($trash, $trash, $trash, $trash, $trash, $trash, $trash, $ipaddress, $trash) = split(/\|/,$filedata);





### Print out the ipadress


$output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 border=0 width=100%>
    <tr>
    <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'2403'} $postmembername</font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle width=30%><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'1452'} $ibtxt{'2404'}:</b></font></td>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$topictitle</font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'0319'}: </b></font></td>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$postdate</font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'2406'}</b></font></td>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$postipaddress</font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'2407'}</b></font></td>
    <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ipaddress</font></td></tr>
    </table></td></tr></table>
    ~;
            
    } # end cleared to edit if
    
    else { # start else
    
### Log in form.    


            $inmembername =~ s/\_/ /g;
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog?forum=$inforum&topic=$intopic&postno=$inpostno&checked=yes" method="post">
            <input type=hidden name="forum" value="$inforum">
            <input type=hidden name="topic" value="$intopic">
            <input type=hidden name="postno" value="$inpostno">
            <input type=hidden name="checked" value="yes">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2408'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize1><b>$ibtxt{'2409'}</b></font></td>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'1417'}</font></a></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
            
            } # end else statement
            
           
&output(
-Title   => "$boardname - $ibtxt{'2412'}", 
-ToPrint => $output, 
-Version => $versionnumber 
);       
            
            
            
