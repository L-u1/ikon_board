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
$CGI::HEADERS_ONCE = 1;                   # Kill redundant headers

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

$thisprog = "ikonboard.cgi";

$query = new CGI;
$action = $query->param('action');

$inmembername = cookie("amembernamecookie");
$inpassword   = cookie("apasswordcookie");


if ($inmembername eq "") {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmemberstime("$inmembername");
        &getlastvisit;
        }

if ($action eq "resetall") {
    $filetoopen = "$ikondir" . "data/allforums.cgi";
    $filetoopen = &stripMETA($filetoopen);
    open(FILE, "$filetoopen") or die "$ibtxt{'5011'}";
      flock(FILE, 1);
    @forums = <FILE>;
    close(FILE);
    $currenttime = time;
    foreach (@forums) { #start foreach @forums
        ($tempno, $trash) = split(/\|/,$_);
        $lvisit .= "$tempno-$currenttime--";
        }

    $cookie     = cookie(-name    =>   "lastvisit",
                         -value   =>   "$lvisit",
                         -path    =>   "$cookiepath",
                         -expires =>   "+30d");
            
    $tempcookie = cookie(-name    =>   "templastvisit",
                         -value   =>   "$lvisit",
                         -path    =>   "$cookiepath");
    print header(-cookie  =>[$cookie, $tempcookie]);
    }
    

    &title;


    require "$ikondir" . "data/boardstats.cgi";
    

    ### Set up the variables for the last registered Member

    $cleanlastregistered = $lastregisteredmember;
    $cleanlastregistered =~ y/ /_/;
    $lastregisteredmember = substr($lastregisteredmember,0,20) if length $lastregisteredmember > 19; 
    $cleanlastregistered = qq~<a href="$profileprog?action=show&member=$cleanlastregistered">$lastregisteredmember</a>~;




    #------- HTML

    $output .= qq~
    <!-- Cgi-bot Begin Board logo and navigation -->
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
        <td width=30% rowspan=2><img src="$imagesurl/images/$boardlogo" border=0></td>
            <td valign=bottom align=right><font face="$font" color=$fontcolormisc size=$dfontsize2>
                $boardname $ibtxt{'0001'} $cleanlastregistered<br>
                $boardname $ibtxt{'0002'} <b>$totalmembers</b> $ibtxt{'0003'} <b>$totalposts</b> $ibtxt{'0004'} <b>$totalthreads</b> $ibtxt{'0024'}
            </td>
        </tr>
    </table>
    <br>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
        <tr>
            <td>
                <table cellpadding=4 cellspacing=1 border=0 width=100%>
            <tr>
            <td bgcolor=$titlecolor width=5% align=center><font face="$font" color=$titlefontcolor size=$dfontsize2><b>&nbsp;</b></td>
            <td bgcolor=$titlecolor width=63%><font face="$font" color=$titlefontcolor size=$dfontsize1><b>$ibtxt{'0006'}</b></td>
            <td bgcolor=$titlecolor width=4% nowrap align="center"><font face="$font" color=$titlefontcolor size=$dfontsize2><b>$ibtxt{'0029'}</b></td>
            <td bgcolor=$titlecolor width=4% nowrap align="center"><font face="$font" color=$titlefontcolor size=$dfontsize2><b>$ibtxt{'2906'}</b></td>
            <td bgcolor=$titlecolor width=25% align="center"><font face="$font" color=$titlefontcolor size=$dfontsize2><b>$ibtxt{'0013'}</b></td>
        </tr>
     <!-- Cgi-bot End Board logo and navigation -->
     ~;

#------- END OF HTML

if ($announcements eq 'yes') {

#------- HTML

        $output .= qq~
        <!-- Cgi-bot Announcements Title -->
        <tr>
            <td bgcolor=$catback colspan=5>
                <font face="$font" color=$catfontcolor size=$dfontsize3>
                <b>&raquo; $ibtxt{'0301'}</b>
                </font>
            </td>
        </tr>
        <!-- Cgi-bot End Announcements Title -->
        ~;

#------- END OF HTML

        my $filetoopen = "$ikondir" . "data/news.cgi";
        if (-e $filetoopen) {
            openFILE(-FH=>'FILE',-FN=>"$filetoopen",-MD=>'r');
            my @announcementdata = <FILE>;
            close(FILE);

            my $totalannouncements = @announcementdata;
            ($title, $dateposted, $trash) = split(/\|/, $announcementdata[0]);
            }
            else { $dateposted = time; $title = $ibtxt{'0031'}; }

        my $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &longdate("$dateposted");

#------- HTML
    
        $output .= qq~
        <!-- Cgi-Bot $ibtxt{'0032'} $dateposted -->
        <tr>
            <td bgcolor=$forumcolortwo align=center>
              <img src="$imagesurl/images/$announce" border=0>
            </td>
            <td bgcolor=$forumcolortwo>
                <font face="$font" color=$forumfontcolor size=$dfontsize2>
                $title
                </font>
            </td>
            <td bgcolor=$forumcolortwo colspan=2 align="center">
                <font face="$font" color=$forumfontcolor size=$dfontsize2>
                [ <a href="$boardurl/$announceprog">$ibtxt{'0033'}</a> ]
                </font>
            </td>
            <td bgcolor=$forumcolorone>
                <font face="$font" color=$forumfontcolor size=$dfontsize1>
                    <b>$dateposted</b>
                </font>
            </td>
        </tr>
        <!-- Cgi-bot End of announcements -->
        ~;

#------- END OF HTML
    
        } 



### Open up the allforums file.

$filetoopen = "$ikondir" . "data/allforums.cgi";
$filetoopen = &stripMETA($filetoopen);
open(FILE, "$filetoopen") or die "$ibtxt{'5012'}";
  flock FILE,1;
@forums = <FILE>;
close(FILE);

foreach $forum (@forums) { #start foreach @forums
    chomp $forum;
    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
    $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forummoderator|$htmlstate|$idmbcodestate|$privateforum|$startnewthreads|$lastposter|$lastposttime|$threads|$posts|$forumgraphic|$forumid");
    push (@rearrangedforums, $rearrange);

} # end foreach (@forums)

@finalsortedforums = sort numerically(@rearrangedforums);

foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

    ($categoryplace, $category, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $forumid) = split(/\|/,$sortedforums);

    if ($forummoderator) {
            $forummoderator =~ s/\, /\,/g;
            my @mods = split(/\,/,$forummoderator);
            my $tm = @mods; my $mc = 1;
            foreach (@mods) {
                my $cmodn = $_; $cmodn =~ y/ /_/;
                if ($mc != $tm) {
                    $modout .= qq~<a href="$boardurl/$profileprog?action=show&member=$cmodn">$_</a>, ~;
                    }
                    else { $modout .= qq~<a href="$profileprog?action=show&member=$cmodn">$_</a>~; }
                $mc++;
                }
            $modout = qq!($ibtxt{'0034'} $modout)!;
            }

    if ($categoryplace ne $lastcategoryplace) {
        $output .= qq~<tr><td bgcolor=$catback colspan=5><font face="$font" color=$catfontcolor size=$dfontsize3><b>&raquo; $category</b></font></td></tr>~;
        }
    
    my $fm = $forumname; $forumname = qq~<a href="$forumsprog?forum=$forumid">$forumname</a>~;
        $forumlastvisit = $lastvisitinfo{$forumid};

        $folderpicture = qq(&nbsp;);
        

if ($advanced_folder eq 'yes'){

        if (($lastposttime > $forumlastvisit) and ($inmembername ne "$ibtxt{'0043'}")) {
            $folderpicture = qq~<img src="$imagesurl/images/$forumid.gif" border="0" align=center>~;
            $posts = qq~<font face="$font" size=$dfontsize2 color=$fonthighlight></b>$posts</b></font><font face="$font" color=$forumfontcolor size=$dfontsize2>~;
            }
            else {
                $folderpicture = qq~<img src="$imagesurl/images/old_$forumid.gif" border="0">~;
                $posts = qq~<font face="$font" color=$forumfontcolor size=$dfontsize2>$posts~;
                }
}#advanced folder
else { 
        if (($lastposttime > $forumlastvisit) and ($inmembername ne "$ibtxt{'0043'}")) {
            $folderpicture = qq~<img src="$imagesurl/images/$foldernew" border="0" align=center>~;
            $posts = qq~<font face="$font" size=$dfontsize2 color=$fonthighlight></b>$posts</b></font><font face="$font" color=$forumfontcolor size=$dfontsize2>~;
            }
            else {
                $folderpicture = qq~<img src="$imagesurl/images/$folder" border="0">~;
                $posts = qq~<font face="$font" color=$forumfontcolor size=$dfontsize2>$posts~;
                }

}# end else ADVANCED FOLDER
        
        if ($inmembername eq "$ibtxt{'0043'}") { $folderpicture = qq(&nbsp;); $loginmessage = "$ibtxt{'0009'}"; }

        $forumlastvisit = $forumlastvisit + ($timedifferencevalue*3600) + ($timezone*3600);
        $lastdate = &longdate("$forumlastvisit");
        $lasttime = &shorttime("$forumlastvisit");
    
    
        if ($lastposttime) {
            $lastposttime = $lastposttime + ($timedifferencevalue*3600) + ($timezone*3600);
            $longdate = &longdate("$lastposttime");
            $shorttime = &shorttime("$lastposttime");
            $forumlastpost = qq~<font size="$dfontsize1" face="$font" color="$lastpostfontcolor">$ibtxt{'0035'} <b>$longdate</b><font size="$dfontsize1" face="$font" color="$lastpostfontcolor"><br>$ibtxt{'0036'} $shorttime</font>~;
            }
        else { $forumlastpost = qq~<font size="$dfontsize1" face="$font" color="$lastpostfontcolor">$ibtxt{'3009'}</font>~; }
        
    $lastposterfilename = $lastposter;
    $lastposterfilename =~ y/ /_/;
    $lastposter =~ y/_/ /;
    
        my @lastpost;
        my ($inforum, $threadnumber, $topictitle);  
        $filetoopen = "$ikondir" . "forum$forumid/lastpost.cgi";
         open(FILE,"$filetoopen");
         flock(FILE,2);
         @lastpost = <FILE>;
         close(FILE);

         
         foreach $lastpost (@lastpost) {
            chomp $lastpost;
            ($inforum, $threadnumber, $topictitle) = split(/\|/,$lastpost);   
            }
            
        if ($inforum eq "") {
        $lastpost = "";
        }
        
        # DimoN
        #elsif ($privateforum eq "yes") {
        #$lastpost = "";
        #}
        
        else {    
        $lastpost = qq~<img src="$imagesurl/images/lastpost.gif"> <a href="$threadprog?forum=$inforum&topic=$threadnumber">$topictitle</a>~;
        }


#------- HTML
    
    $output .= qq~
    <!-- Cgi-bot Forum $fm entry -->
    <tr>
        <td bgcolor=$forumcolortwo align=center>
            $folderpicture
        </td>
        <td bgcolor=$forumcolortwo align="left">
            <font face="$font" color="$forumfontcolor" size=$dfontsize3>
            <b>$forumname</b>
            </font>
            <font face="$font" color="$forumfontcolor" size=$dfontsize2>
            <br>$forumdescription
            </font>
            <font face="$font" color="$fonthighlight" size=$dfontsize1>
            <br>$modout
            </font>
        </td>
        <td bgcolor=$forumcolortwo align="center" valign=middle>
            <font face="$font" color=$forumfontcolor size=$dfontsize2>
            $posts
        </td>
        <td bgcolor=$forumcolortwo align="center" valign=middle>
            <font face="$font" color=$forumfontcolor size=$dfontsize2>
            $threads
        </td>
        <td bgcolor=$forumcolorone align=left valign=middle>
            <font color=$lastpostfontcolor face="$face" size="$dfontsize2">
            $forumlastpost
    ~; 

# Скрываем ластпост в закрытых форумах
    &getmember("$inmembername"); 
    if ("$privateforum" ne "yes" || $membercode eq "ad" || $membercode eq "mo") { 
    $output .= qq~ 
            <br>$lastpost
            <br>$ibtxt{'0616'} <a href="$profileprog?action=show&member=$lastposterfilename">$lastposter</a>
    ~;  }  
    
    $output .= qq~    
            </font>
        </td>
    </tr>
    <!-- Cgi-bot End of Forum $fm entry -->
    ~;

#------- END OF HTML
    
    $lastcategoryplace = $categoryplace;
    undef $forumlastvisit; undef $forummoderator; undef $modout;
    }


    &whosonline("$inmembername|$ibtxt{'0015'}|$ibtxt{'0016'}");
    my $total_users = $guests + $members;
    
#------- HTML
if ($online_ ne "off"){
  if ($online_ eq "on"){
  $online_header = qq~<b>$total_users чел. за последние $membergone минут был(и) на конференции:</b>~;
  $online_row = qq~$ibtxt{'0019'} $guests, $ibtxt{'0020'} $members <br><font face="$font" color=$forumfontcolor size=$dfontsize1>$memberoutput~;
  }
  if ($online_ eq "reg" && $membername eq "$ibtxt{'0043'}"){
  $online_header = qq~<b>Кто в онлайн.</b>~;
  $online_row = qq~Вы должны <a href="$registerprog">зарегистрироваться</a> чтобы видеть кто в онлайне.~;
  } else {
          $online_header = qq~<b>$total_users чел. за последние $membergone минут был(и) на конференции:</b>~;
          $online_row = qq~$ibtxt{'0019'} $guests, $ibtxt{'0020'} $members <br><font face="$font" color=$forumfontcolor size=$dfontsize1>$memberoutput~;
          }
    $output .= qq~
    <!-- Cgi-bot Active Users -->
    <tr>
        <td bgcolor=$titlecolor colspan=5>
            <font face="$font" color=$titlefontcolor size=$dfontsize2>
            $online_header
            </font>
        </td>
    </tr>
    <tr>
        <td bgcolor=$forumcolortwo>
            <img src="$imagesurl/images/$online" border=0 width=20 height=20 align=center>
        </td>
        <td bgcolor=$forumcolortwo colspan=4>
            <font face="$font" color=$forumfontcolor size=$dfontsize1>
            $online_row</font>
        </td>
    </tr>
    <!-- Cgi-bot End of Active Users -->
    ~;
    }
    $output .= qq~
    </table>
    </td>
    </tr>
    </table>
    ~;

#------- END OF HTML

    if ($loginmessage) {

#------- HTML

        $output .= qq~
        <!-- Cgi-bot Script page footer -->
        <p>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
            <tr>
                <td>
                    <font face="$font" color=$fontcolormisc size=$dfontsize1>
                    <p>$ibtxt{'0021'} $basetimes<p>$loginmessage
                    </font>
                </td>
            </tr>
        </table>
        <!-- Cgi-bot End of script page footer -->
        ~;
    
        }
        else {

        $output .= qq~
        <!-- Cgi-bot Script page footer -->
        <p>
        <table cellpadding=0 cellspacing=4 border=0 width=$tablewidth align=center>
            <tr>
                <td align=left colspan=2 valign=top>
                    <font face="$font" color=$fontcolormisc size=$dfontsize1>
                    $ibtxt{'0021'} $basetimes<p>
                    </font>
                </td>
            </tr>
            <tr>
                <td width=5% align=center>
                    <img src="$imagesurl/images/$foldernew" border=0>
                </td>
                <td align=left>
                    <font face="$font" color=$fontcolormisc size=$dfontsize1>
                    $ibtxt{'0022'}
                    </font>
                </td>
            </tr>
            <tr>
                <td width=5% align=center>
                    <img src="$imagesurl/images/$folder" border=0>
                </td>
                <td align=left>
                    <font face="$font" color=$fontcolormisc size=$dfontsize1>
                    $ibtxt{'0023'}
                    </font>
                </td>
            </tr>
        </table>
        <!-- Cgi-bot End of script page footer -->
        ~;

#------- END OF HTML

        }

print header('text/html; charset=windows-1251');
&output(
-Title   => $boardname, 
-ToPrint => $output, 
-Version => $versionnumber 
);







