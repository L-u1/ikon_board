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

$thisprog = "printpage.cgi";

$query = new CGI;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');

print header('text/html; charset=windows-1251');

if (($inforum)  && ($inforum !~ /^[0-9]+$/))  { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($intopic ) && ($intopic  !~ /^[0-9]+$/)) { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }
if (($number)   && ($number !~ /^[0-9]+$/))   { &error("$ibtxt{'0901'}&$ibtxt{'0501'}."); }

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = cookie("apasswordcookie"); }

if ($inmembername eq "" || $inmembername eq "$ibtxt{'0043'}" ) {
    $inmembername = "$ibtxt{'0043'}";
        }
        else { 
            &getmember("$inmembername");
            if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; } else { $allowed = "no"; }
                &getmemberstime("$inmembername");
                &getlastvisit;
                $forumlastvisit = $lastvisitinfo{$inforum};
                $currenttime = time;
                &setlastvisit("$inforum,$currenttime");
                }
$filetoopen = "$ikondir" . "data/allforums.cgi";
open(FILE, "$filetoopen");
  flock(FILE, 2);
@forums = <FILE>;
close(FILE);
foreach $forumline (@forums) {
    ($tempno, $trash) = split(/\|/,$forumline);
    if ($inforum eq $tempno) {
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forumline);
        }
    }
if (("$privateforum" eq "yes") && ("$allowed" ne "yes")) {
    &error("$ibtxt{'1606'}&$ibtxt{'1607'}");
    }
    else {
        &whosonline("$inmembername|$ibtxt{'1601'} <a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a> in <a href=\"$forumsprog?forum=$inforum\"><b>$forumname</b></a>|$ibtxt{'1602'}");
        }

### Grab the topic title

    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
    open(FILE, "$filetoopen");
    @threads = <FILE>;
    close(FILE);

    ($trash, $topictitle, $trash) = split(/\|/, @threads[0]);
    

    $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
    


### Print the header


    $output .= qq~
    <html><head><title>$boardname $ibtxt{'1603'} Ikonboard</title></head>
    <body topmargin=10 leftmargin=0>
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
        <tr>
            <td>
            <p><b>$ibtxt{'1604'}</b><p>
            <b>-$boardname</b> ($boardurl/$forumsummaryprog)<br>
            <b>--$forumname</b> ($boardurl/$forumsprog?forum=$inforum)<br>
            <b>---$topictitle</b> ($boardurl/$forumsprog?forum=$inforum&topic=$intopic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 border=0 width=90% align=center>
        <tr>
            <td>
            
    ~;
    foreach $line (@threads) {
    
        
        ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\|/,$line);
    
        $post = &ikoncode("$post");
    
        $post =~ s/&lt\;/\</g;
        $post =~ s/&gt\;/\>/g;
        $post =~ s/&quot\;/\"/g;
    
        $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
    
        $output .= qq~
        <p>
        <hr><p>
        -- $ibtxt{'1605'} $postermembername $ibtxt{'1119'} $postdate<p>
        $post
        <p><p>
        ~;
    
    } # end foreach
    
    
    $output .= qq~
        </td></tr></table><center><hr><p>$boardname $ibtxt{'1603'} Ikonboard<br>http://www.ikonboard.com<br>&copy; 2000 Ikonboard.com</center>
        </body></html>
        ~;
                    


    
    print $output;
    
    exit;       
            
