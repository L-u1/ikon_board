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

$thisprog = "forums.cgi";


$query = new CGI;

$cookiepath     = $query->url(-absolute=>1);
$cookiepath     =~ s/$thisprog//sg;
$bypass         = $query -> param('bypass');
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
$action         = $query -> param('action');
$inshow         = $query -> param('show');
$jumpto         = $query -> param('jumpto');
die "Hack attempt!" unless $inforum =~ m!\A\d{1,3}\Z!;
die "Hack attempt!" if $intopic && $intopic !~ m!\A\d{1,7}\Z!;


$inmembername   = cookie("amembernamecookie");
$inpassword     = cookie("apasswordcookie");

$bypass         = &stripMETA("$bypass");
$inforum        = &stripMETA("$inforum");
$intopic        = &stripMETA("$intopic");
$action         = &stripMETA("$action");
$inshow         = &stripMETA("$inshow");
$jumpto         = &stripMETA("$jumpto");

              
if ((!$inmembername) or ($inmembername eq "$ibtxt{'0043'}")) {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
        }


if ($action eq "accessrequired") {
    $inmembername  = $query -> param('membername');
    $inpassword    = $query -> param('password');
    &getmember("$inmembername");
    if ($userregistered ne "no" && $allowedentry{$inforum} eq "yes" && $inpassword eq $password) {
        $allowcookiename = "forumsallowed" . "$inforum";
        print "Set-Cookie: $allowcookiename=yes\;";
        print "\n";
        $allowed = "yes";
        }
        else {
            $allowed = "no";
            }
        }
        else {
            $tempaccess = "forumsallowed". "$inforum";
            $testentry = cookie("$tempaccess");
            if ($testentry eq "yes") { $allowed = "yes"; }
            else { $allowed = "no"; }
            }




if ($action eq "resetposts") {
    $currenttime = time;
    $currenttime = ($currenttime+10);
    $mv=1; &setlastvisit("$inforum,$currenttime");
    print redirect(-location=>"$boardurl/$thisprog?forum=$inforum",
                   -cookie=>[$tempvisitcookie, $permvisitcookie]);
    exit;
    }

print header(-cookie=>[$tempvisitcookie, $permvisitcookie]);

&forumjump;

if ($jumpto) {
    print redirect(-location=>"$jumpto");
    exit;
    }


        &getforum("$inforum");

        # define the thread button/forumgraphic, forum moderator and thread age menu

        $newthreadbutton = qq~<a href="$postprog?action=new&forum=$inforum"><img src="$imagesurl/images/newthread.gif" border="0"></a>~;
        
        if ($forumgraphic) {
        $forumgraphic = qq~<a href="$forumsprog?forum=$inforum"><img src="$imagesurl/images/$forumgraphic" border=0></a>~;
        }
        else { $forumgraphic = qq~<a href="$forumsprog?forum=$inforum"><img src="$imagesurl/images/$boardlogo" border=0></a>~; }
        
        &moderator;
        
        &title;
        
        # Print the header

        $output .= qq~
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
                <tr>
                    <td width=30% rowspan=2>$forumgraphic
                       </td>
                       <td align=left valign=top><font face="$font" color=$fontcolormisc size=$dfontsize2>
                            <font face="$font" color=$fontcolormisc size=$dfontsize2>
	                        &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	                        <br>
                            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$forumname
                       </td>
                </tr>
            $uservisitdata
        </tr>
        </table>
        <br>
        ~;

    # Check if it's a private forum, and is the member cleared?

    if (("$privateforum" eq "yes") && ("$allowed" ne "yes"))  { &accessneeded; }

    if (($inmembername) && ($privateforum ne "yes")) { &whosonline("$inmembername|$ibtxt{'0617'} <a href=\"$forumsprog?forum=$inforum\"><b>$forumname</b></a>|$ibtxt{'1602'}"); }
        
    # Open up the forum threads list

    $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
    $filetoopen = &stripMETA($filetoopen);
    if (-e $filetoopen) {
        open(FILE, "$filetoopen") or &error("$ibtxt{'0618'}&$ibtxt{'0619'}");
          flock (FILE, 2);
        @topics = <FILE>;
        close(FILE);
        }

    # Limit the total topics to a span

    $numberofitems = @topics;
    $maxtopics = 15;
    $numberofpages = $numberofitems / $maxtopics;
    
    if ($numberofitems > $maxtopics) { #if
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) { $inshow = 0; }
        if ($inshow > 0) { $startarray = $inshow; }
            else { $startarray = 0; }
            $endarray = $inshow + $maxtopics - 1;
            if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
            elsif (($endarray > ($maxtopics - 1)) && ($more ne "yes")) { $endarray = $numberofitems - 1; }
            } #
            else {
                $showmore = "no";
                $startarray = 0;
                $topicpages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1>$ibtxt{'0602'}</font>~;
                $toptopicpages = $topicpages;
                $endarray = @topics - 1;
                }

    # if we have multiple pages, print them
    
        if ($showmore eq "yes") { #1
            if ($maxtopics < $numberofitems) { #2
                ($integer,$decimal) = split(/\./,$numberofpages);
                    if ($decimal > 0) { $numberofpages = $integer + 1; }
                        $pagestart = 0;
                        $counter = 0;
                            while ($numberofpages > $counter) { #3
                                $counter++;
                                if ($inshow ne $pagestart) { $pages .= qq~<a href="$thisprog?forum=$inforum&show=$pagestart"><font face="$font" color=$fonthighlight size=$dfontsize1><b>$counter</b></font></a> ~; }
                                 else { $pages .= qq~<a href="$thisprog?forum=$inforum&show=$pagestart"><font face="$font" color=$menufontcolor size=$dfontsize1>$counter</font></a> ~; }
                                $pagestart = $pagestart + $maxtopics;
                                } #e3
                            } #e2
                $topicpages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1><b>$ibtxt{'0603'}</b> [ $pages ]~;
                } #1

        

        # Limit the pages output at the top, so we don't distort the tables

        if ($numberofpages > 10) {
            $toptopicpages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1><b>$ibtxt{'0603'}</b> [ $ibtxt{'0620'} ]~;
            }
            else {
                $toptopicpages = $topicpages;
                }
        
        # Print the forum top bar

        $output .= qq~
            <table cellpadding=0 cellspacing=1 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
                <td>
            <table cellpadding=6 cellspacing=0 border=0 width=100%>
                <tr>
                  <td valign=middle align=left width="100%" bgcolor="$menubackground" nowrap>$toptopicpages</td>
                  <td valign=middle align=right bgcolor="$menubackground" nowrap><font face="$font" color=$fontcolormisc size=$dfontsize1>
                   <b>$ibtxt{'0604'}</b> $modoutput
                    </td>
                </tr>
           </table>
           </tr>
          </td>
         </table>
        <br>
        ~;

        

        

        # Start printing the threads

        $output .= qq~
                <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                 <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                   <td bgcolor=$titlecolor width=50% colspan=2><font face="$font" color=$titlefontcolor size=$dfontsize1><b>$newthreadbutton</b></td>
                    <td bgcolor=$titlecolor align=left width=25%><font face="$font" color=$titlefontcolor size=$dfontsize1><b>$ibtxt{'0621'}</b></td>
                   <td bgcolor=$titlecolor width=25%><font face="$font" color=$titlefontcolor size=1><b>$ibtxt{'0013'}</b></td>
                </tr>
                ~;



        # Grab the threads to show


        foreach $topic (@topics[$startarray ... $endarray]) { # start topic foreach
                chomp $topic;
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$topic);
                
                
        
        
        # Span time, yet again. Who needs sub-routes?
        
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

                
                                

                                # Forum Post markers


                                if (!$forumlastvisit) { $forumlastvisit = "0"; }
                                
                                $topicicon = "<img src=\"$imagesurl\/images\/$topichotnonew\" border=\"0\">";
                                
                                if (($threadposts => $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "$ibtxt{'0043'}")) {
                                        $topicicon = "<img src=\"$imagesurl\/images\/$topichot\" border=\"0\">";
                                        }
                                if (($threadposts => $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "$ibtxt{'0043'}")) {
                                        $topicicon = "<img src=\"$imagesurl\/images\/$topichotnonew\" border=\"0\">";
                                        }
                                if (($threadposts < $hottopicmark) && ($forumlastvisit < $lastpostdate) && ($inmembername ne "$ibtxt{'0043'}")) {
                                        $topicicon = "<img src=\"$imagesurl\/images\/$topicnew\" border=\"0\">";
                                        }
                                if (($threadposts < $hottopicmark) && ($forumlastvisit > $lastpostdate) && ($inmembername ne "$ibtxt{'0043'}")) {
                                        $topicicon = "<img src=\"$imagesurl\/images\/$topicnonew\" border=\"0\">";
                                        }
                                
                                unless ($threadstate ne "closed") {
                                        $topicicon = "<img src=\"$imagesurl\/images\/$topiclocked\" border=\"0\">";
                                        }
                        
                        
                        if ($lastpostdate ne "") {
                        $lastpostdate = $lastpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
                        $longdate = &longdate("$lastpostdate");
                        $shorttime = &shorttime("$lastpostdate");
                        $lastpostdate = qq~<font size="$dfontsize1" face="$font" color="$fontcolormisc">$longdate - <font size="$dfontsize1" face="$font" color="$fontcolormisc">$shorttime~;
                        }
                        else {
                                $lastpostdate = qq~<font size="$dfontsize1" face="$font" color="$fontcolormisc">$ibtxt{'3009'}~;
                                        $lastpoststamp = "";
                                }
                        $startedpostdate = $startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600);
                        $startedlongdate = &shortdate("$startedpostdate");
                        $startedshorttime = &shorttime("$startedpostdate");
                        $startedpostdate = qq~<font size="$dfontsize1" face="$font" color="$fontcolormisc">$startedlongdate~;
        
                        $topictitle = qq~<a href="$threadprog?forum=$inforum&topic=$topicid">$topictitle</a>~;
        
                        $startedbyfilename = $startedby;
                        $startedbyfilename =~ s/ /\_/isg;
                        
                        $lastposterfilename = $lastposter;
                        $lastposterfilename =~ s/ /\_/isg;
                        $lastposter = qq~<a href="$profileprog?action=show&member=$lastposterfilename">$lastposter</a>~;
                
                        if ($topicdescription) { $topicdescription = qq~&nbsp;&nbsp;&raquo;$topicdescription~; } 
                        
                        $output .=qq~
                                <tr>
                                <td bgcolor=$forumcolortwo width=5% align=center><font face="$font" color=$forumfontcolor size=$dfontsize2>$topicicon</td>
                                <td bgcolor=$forumcolortwo width=40%><font face="$font" color=$forumfontcolor size=$dfontsize2><b>$topictitle</b> $pagestoshow<br><font size=$dfontsize1>$topicdescription</font></td>
                                <td bgcolor=$forumcolortwo align=left valign=middle><font face="$font" color=$forumfontcolor size=$dfontsize1><b>$threadposts</b> $ibtxt{'0011'}, $ibtxt{'0601'} <b>$threadviews</b> $ibtxt{'0614'}
                                <br>$ibtxt{'0615'} <a href="$profileprog?action=show&member=$startedbyfilename"><b>$startedby</b></a></td>
                                <td bgcolor=$forumcolorone><font face="$font" color=$forumfontcolor size=$dfontsize2>$lastpostdate<br>$ibtxt{'0616'} <b>$lastposter</b></td>
                                </tr>
                                ~;
                        $pagestoshow = undef;
                        $threadpages = undef;
                
                } # end topic foreach
                
        $output .= qq~
        <tr>
        <td bgcolor=$titlecolor colspan=4><font face="$font" color=$titlefontcolor size=$dfontsize1><b>$newthreadbutton</b></td>
        </tr></table></td>
        </tr></table>
        <table align=center width=$tablewidth bgcolor=$menubackground><tr>
        <td align=left>$topicpages</td><td align=right>$jumphtml</td></tr></table>
        
    ~; 
	&getmember("$inmembername"); 
	if ($membercode eq "ad" || $membercode eq "mo") { 
	$output .= qq~ 
        
        <table align=center width=$tablewidth>
        <tr>
        <td align=right><font face="$font" color=$menufontcolor size=$dfontsize1>
        $ibtxt{'0623'} <a href="$forumoptionsprog?action=prune&forum=$inforum">$ibtxt{'0622'}</a>
        </td>
        </tr>
        </table>
    ~;    
	}        
	$output .= qq~ 
        
        <table align=center width=$tablewidth>
        <tr>
        <td align=left><img src="$imagesurl/images/$topiclocked" border="0"></td>
        <td align=left><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0606'}</font></td>
        </tr>
        <tr>
        <td align=left><img src="$imagesurl/images/$topicnonew" border="0"></td>
        <td align=left><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0607'}</font></td>
        </tr>
        ~;
        
        if ($inmembername ne "$ibtxt{'0043'}") {
        
                $output .= qq~
                <tr>
                <td align=left><img src="$imagesurl/images/$topicnew" border="0"></td>
                <td align=left><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0608'}</font></td>
                </tr>
                <tr>
                <td align=left valign=middle><img src="$imagesurl/images/$topichot" border="0">&nbsp;<img src="$imagesurl/images/$topichotnonew" border="0"></td>
                <td align=left><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0609'} $hottopicmark $ibtxt{'0011'}</font></td>
                </tr>
                ~;
                }
                
        $output .= qq~</table><p><p>~;
        
        $output =~ s/value=\"$inthreadages\"/value=\"$inthreadages\" selected/;
        
&output(
-Title   => "$boardname &gt; $category &gt; $forumname", 
-ToPrint => $output, 
-Version => $versionnumber 
);

        

#### Access needed form

sub accessneeded {

        $output .= qq~
        <form action="$thisprog" method=POST>
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="action" value="accessrequired">
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                 <td>
                  <table cellpadding=3 cellspacing=1 border=0 width=100%>
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=4 align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'0611'}</b></font></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle colspan=4><font face="$font" color=$fontcolormisc size=$dfontsize1>
        <br>$ibtxt{'0612'}<br>
        $ibtxt{'0613'}<p></td>
        </tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0306'}</font></td>
        <td bgcolor=$miscbackone valign=middle colspan=2><input type=text name="membername" value="$inmembername" size=20> &nbsp; <a href="$registerprog"><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'1417'}</font></a></td></tr>
        <tr>
        <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc size=$dfontsize1>$ibtxt{'0307'}</font></td>
        <td bgcolor=$miscbackone valign=middle colspan=2><input type=password name="password" value="$inpassword" size=20> &nbsp; <font face="$font" color=$fontcolormisc size=$dfontsize1><a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td></tr>
        <tr>
        <td bgcolor=$miscbacktwo valign=middle colspan=4 align=center><input type=submit name="submit" value="$ibtxt{'0104'}"></td></tr></table></td></tr></table>
       </form>
        ~;      
        
        &output(
        -Title   => "$boardname", 
        -ToPrint => $output, 
        -Version => $versionnumber 
        );

        }
