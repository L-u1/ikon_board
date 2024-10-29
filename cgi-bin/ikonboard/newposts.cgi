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

$thisprog = "newposts.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

$action                 = $query -> param('action');
$inmembername           = $query -> param("membername");
$inpassword             = $query -> param("password");
$inmembername           = &cleaninput($inmembername);
$inpassword             = &cleaninput($inpassword);


if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }

    if ($inmembername eq "") {
      $inmembername = "$ibtxt{'0043'}";
      }
      else {
           &getmemberstime("$inmembername");
           }

if ($action eq "viewposts") {
$namecookie = cookie(-name    =>   "amembernamecookie",
                     -value   =>   "$inmembername",
                     -path    =>   "$cookiepath",
                     -expires =>   "+30d");
$passcookie = cookie(-name    =>   "apasswordcookie",
                     -value   =>   "$inpassword",
                     -path    =>   "$cookiepath",
                     -expires =>   "+30d");

print header(-cookie  =>[$namecookie, $passcookie]);
}
else {
print header('text/html; charset=windows-1251');
    }


    ### Print Header for the page.

    $output .= qq~
    <table cellpadding=0 cellspacing=0 border=0 width=95% bgcolor=$tablebordercolor align=center>
        <tr>
            <td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                    <tr>
                        <td bgcolor=$miscbacktwo align=center colspan=3><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'1304'}</b></td>
                    </tr>
                    <tr>
                        <td bgcolor=$miscbackone valign=middle align=center colspan=3><font face="$font" color=$fontcolormisc size=$dfontsize1>
                        <br><br>$ibtxt{'1301'}<br><br>
                        
                        </td>
                    </tr>
                    ~;
            
                    
    
    if ($action eq "viewposts") {
    
    
    # Validate user
    
    &getmember("$inmembername");
    
    if    ($userregistered eq "no")  { &messengererror("$ibtxt{'0107'}&$ibtxt{'1102'}"); }
    elsif ($inpassword ne $password) { &messengererror("$ibtxt{'0107'}&$ibtxt{'0303'}"); }
    elsif ($inmembername eq "")      { &login("$thisprog?action=viewposts"); }
        
    # Lets grab the current forums
                    
    $filetoopen = "$ikondir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen");
      flock FILE,1;
    @forums = <FILE>;
    close(FILE);

    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
        
        # Trim some fat off the search. If the poster doesn't have access, or has never been to a forum
        # or has visited since, and no new posts found - move on to the next forum
        
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$forumid};
        if ($forumlastvisit eq "0" || $forumlastvisit eq "") { next; }
        if ($forumlastvisit > $lastposttime) { next; }
        if (($privateforum eq "yes") && ($allowedentry{$forumid} ne "yes")) { next; }
        
        $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic|$forumid");
        push (@rearrangedforums, $rearrange);
        
        } # end foreach (@forums)


        @finalsortedforums = sort numerically(@rearrangedforums);
        
        # Lets search through the remaining forums with new posts.
        
        foreach (@finalsortedforums) {
        
            ($categoryplace, $category, $forumname, $forumdescription,$forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $forumid) = split(/\|/,$_);
        
            $filetoopen = "$ikondir" . "forum$forumid/list.cgi";
            $filetoopen = &stripMETA($filetoopen);
            open(FILE, "$filetoopen");
	          flock FILE, 1;
            @topics = <FILE>;
            close(FILE);

    
            foreach $topic (@topics) { # start topic foreach
                chomp $topic;
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$topic);
        
                if ($forumlastvisit < $lastpostdate) {
                    $found = ("$categoryplace|$category|$forumid|$topicid|$forumname|$topictitle|$lastposter|$lastpostdate");
                    push (@founditems, $found);
                    }
                    
            } # end foreach @topics
            
        } # end foreach @finalsortedforums
    
    
    
    # if none are found...
    
    $totals = @founditems;
    
    if ($totals eq 0) {
        $output .= qq~<tr><td bgcolor=$forumcolortwo colspan=4><font face="$font" color=$forumfontcolor size=$dfontsize2><b>$ibtxt{'1302'}</b>
        <br><br>$ibtxt{'1303'}</font></td></tr>\n~;
        }
    
    
    # Otherwise, lets print the results
    
    foreach (@founditems) {
    
    ($categoryplace, $categoryname, $forumid, $topicid, $forumname, $topictitle, $lastposter, $lastpostdate) = split (/\|/,$_);
    
        if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
            $output .= qq~<tr><td bgcolor=$catback colspan=4><font face="$font" color=$catfontcolor size=$dfontsize3><b>$categoryname</b></font></td></tr>\n~;
            } 
        if ($forumid ne $lastforumid) { #start if $forumid
            $output .= qq~<tr><td bgcolor=$forumcolortwo colspan=4><font face="$font" color=$forumfontcolor size=$dfontsize2><b>&raquo; $forumname</b></font></td></tr>\n~;
            }
        
        $lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $longdate = &longdate("$lastpostdate");
        $shorttime = &shorttime("$lastpostdate");
        $topiclastpost = qq~<font size="$dfontsize1" face="$font" color="$lastpostfontcolor">$longdate $ibtxt{'0010'} <font size="$dfontsize1" face="$font" color="$lastpostfontcolor">$shorttime</font>~;
        
        
        $output .= qq~
                    <tr>
                        <td bgcolor=$forumcolortwo><font face="$font" color=$forumfontcolor size=$dfontsize1><a href="$threadprog?forum=$forumid&topic=$topicid" target="_source">$topictitle</a></td>
                        <td bgcolor=$forumcolortwo><font face="$font" color=$forumfontcolor size=$dfontsize1>$ibtxt{'1305'} $lastposter --> $topiclastpost</td>
                    </tr>
                    ~;
                    
        $lastcategoryplace = $categoryplace;
        $lastforumid = $forumid;
        
        
        } # end foreach
        
    
    
    } # end action
    
    
    else {
    
        &login("$thisprog?action=viewposts");
        
        }               
                    
                    
    $output .= "</table></td></tr></table>\n";
    
            &printmessenger(
            -Title   => "$boardname - $ibtxt{'1306'}", 
            -ToPrint => $output, 
            -Version => $versionnumber 
            );

    
    
sub login {

	local($url) = @_;
	
    ($postto, $therest) = split(/\?/,$url);
    
    @pairs = split(/\&/,$therest);
    
    foreach (@pairs) {
        ($name, $value)=split(/\=/,$_);
        $hiddenvars .= qq~<input type=hidden name="$name" value="$value">\n~;
        }
           
	        
	    $output .= qq~
	    <form action="$postto" method="post">$hiddenvars
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0801'}</b></font></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0727'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
	            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
	        <tr>
	            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></form></td></tr></table></td></tr></table>
	        ~;
	        
	 } # end routine        
	        
	 

