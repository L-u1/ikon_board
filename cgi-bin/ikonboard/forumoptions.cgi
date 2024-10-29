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

$thisprog = "forumoptions.cgi";



$query = new CGI;

&checkVALIDITY;
	
$checked        = $query -> param('checked');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$prunedays      = $query -> param('prunedays');
$inmembername   = $query -> param('membername');
$inpassword     = $query -> param('password');

$inforum        = &stripMETA("$inforum");
$intopic        = &stripMETA("$intopic");
$action         = &stripMETA("$action");
$prunedays      = &stripMETA("$prunedays");
$inmembername   = &stripMETA("$inmembername");
$inpassword     = &stripMETA("$inpassword");

print header('text/html; charset=windows-1251');

if (($inforum  !~ m|([0-9\G]+$)|g) or (!$inforum))  { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($prunedays) && ($prunedays !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }


if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }


&moderator;
        


if ($action eq "prune") {

    &getmember("$inmembername");
    &moderator;

    &error("$ibtxt{'0503'}&$ibtxt{'0515'}") if (!$inmembername);
    &error("$ibtxt{'0503'}&$ibtxt{'0515'}") if (!$inpassword);
    &error("$ibtxt{'0503'}&$ibtxt{'0514'}") if ($userregistered eq "no");

    $cleartoedit = "no";
    
    
    &mischeader("$ibtxt{'0510'}");

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    
        if ($cleartoedit eq "no" && $checked eq "yes") { &error("$ibtxt{'0503'}&$ibtxt{'0504'}"); }
        if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        
        if (! $prunedays) {  &error("$ibtxt{'0503'}&$ibtxt{'0505'}"); }      

        ### Grab the list from the forum folder.

        $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen") or die "$ibtxt{'0326'}";
          flock FILE, 1;
        @topics = <FILE>;
        close(FILE);

        foreach (@topics) {
            ($topicid, $tr, $tr, $tr, $tr, $tr, $tr, $tr, $tr, $lastpostdate) = split(/\|/,$_);
            $currenttime = time;
            $threadagelimit = $currenttime - ($prunedays * 86400);
            if ($lastpostdate < $threadagelimit) {
               
                  $filetoopen  = "$ikondir" . "forum$inforum/$topicid.thd";
                  $filetoopen = &stripMETA($filetoopen);
                  open (FILE, "$filetoopen");
                  @temppostcount = <FILE>;
                  close (FILE);

                  $postcount = @temppostcount;
                  $postcount--;
      
                  $filetotrash = "$ikondir" . "forum$inforum/$topicid.thd";
                  unlink $filetotrash;
                  $filetotrash = "$ikondir" . "forum$inforum/$topicid.mal";
                  unlink $filetotrash;
                  $filetotrash = "$ikondir" . "forum$inforum/$topicid.pl";
                  unlink $filetotrash;
   
                  $totaltopics_deleted++;
                  $totalposts_deleted = $totalposts_deleted + $postcount;
                  }
            }
  

        ### Recreate the list:

        rebuildLIST(-Forum=>"$inforum");

        ### Update the post counts
        
        $filetoopen = "$ikondir" . "data/allforums.cgi";
        $filetoopen = &stripMETA($filetoopen);
        open(FILE, "$filetoopen") or die "$ibtxt{'0326'}";
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
                    $posts = $posts - $totalposts_deleted;
                    $threads = $threads - $totaltopics_deleted;
                    $processed_data .= "$forumid|$category|$categoryplace|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic\n";
                }
            else { $processed_data .= "$forum\n"; }
        }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        open(FILE, ">$filetomake") or die "$ibtxt{'0326'}";
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;
        
        
        require "$ikondir" . "data/boardstats.cgi";
        
        $filetomake = "$ikondir" . "data/boardstats.cgi";
        
        $totalthreads = $totalthreads - $totaltopics_deleted;
        $totalposts = $totalposts - $totalposts_deleted;
        
        open(FILE, ">$filetomake") or die "$ibtxt{'0326'}";
          flock(FILE, 2);
        print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
        print FILE "\$totalmembers = \"$totalmembers\"\;\n";
        print FILE "\$totalthreads = \"$totalthreads\"\;\n";
        print FILE "\$totalposts = \"$totalposts\"\;\n";
        print FILE "\n1\;";
        close (FILE);

            if (! $totaltopics_deleted) { $totaltopics_deleted = "no"; }
            if (! $totalposts_deleted)  { $totalposts_deleted  = "no"; }
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>    
            <td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'0506'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>
            $ibtxt{'1004'}:
            <ul>
            <li>$totaltopics_deleted $ibtxt{'2949'}
            <li>$totalposts_deleted $ibtxt{'0508'}
            <li><a href="$forumsprog?forum=$inforum">$ibtxt{'0509'}</a>
            <li><a href="$forumsummaryprog">$ibtxt{'1012'}</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            ~;

            } # end if clear to edit
            

            else {
            
            &mischeader("$ibtxt{'0510'}");
            
            $output .= qq~
            <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 border=0 width=100%>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="prune">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$inforum">
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'0511'}</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'0512'}</b>
            <br>$ibtxt{'0513'}</font></td>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0306'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="membername" value="$inmembername" size=20></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0307'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=password name="password" value="$inpassword" size=20></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1>$ibtxt{'0516'}</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="prunedays" size=20></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            ~;
            
             }

} # end massprune

else { &error("$ibtxt{'0517'}&$ibtxt{'0518'}"); }



&output(
    -Title   => "$boardname-$ibtxt{'0510'}", 
    -ToPrint => $output, 
    -Version => $versionnumber 
    );


