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

use CGI::Carp "fatalsToBrowser";
use CGI qw(:standard);
$CGI::POST_MAX=1024 * 150;
$CGI::DISABLE_UPLOADS = 1;

eval {
($0 =~ m,(.*)/[^/]+,)   && unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) && unshift (@INC, "$1");
require "ikon.lib";
require "data/progs.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
    }

$|++;

#################--- Begin the program ---###################

$thisprog = "topic.cgi";

$query = new CGI;
$cookiepath     = $query->url(-absolute=>1);
$cookiepath     =~ s/$thisprog//sg;
$inforum        = $query -> param('forum');
$inforum        = &stripMETA("$inforum");
$intopic        = $query -> param('topic');
$intopic        = &stripMETA("$intopic");
$instart        = $query -> param('start');
$instart        = &stripMETA("$instart");
$jumpto         = $query -> param('jumpto');
$jumpto         = &stripMETA("$jumpto");
die "Hack attempt!" unless $inforum =~ m!\A\d{1,3}\Z!;
die "Hack attempt!" if $intopic && $intopic !~ m!\A\d{1,7}\Z!;
$inmembername   = cookie("amembernamecookie");
$inpassword     = cookie("apasswordcookie");



&forumjump;
if ($jumpto) {
    print redirect(-location=>"$jumpto"); exit;
    }
if ((!$inmembername)||($inmembername eq Guest)) {
    $inmembername = "$ibtxt{'0043'}";
    }
    else {
        &getmember("$inmembername");
        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
            else { $allowed  = "no"; }
       # &getmemberstime("$inmembername");
       #Не нужен вызов, делали до этого getmember
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
        }

    print header(-cookie=>[$tempvisitcookie, $permvisitcookie]);

    &getforum($inforum);

    if ($forumgraphic) { $forumgraphic = qq~<a href="$forumsprog?forum=$inforum"><img src="$imagesurl/images/$forumgraphic" border=0></a>~; }
        else { $forumgraphic = qq~<a href="$boardurl/$forumsummaryprog"><img src="$imagesurl/images/$boardlogo" border=0></a>~; }

    $filetoopen = "$ikondir" . "forum$inforum/list.cgi";
    $filetoopen = &stripMETA($filetoopen);
    if (-e $filetoopen) {
        open(FILE, $filetoopen) or &error("$ibtxt{'3001'}&$ibtxt{'3002'}$inforum/list.cgi");
          flock (FILE, 1);
        @allthreads = <FILE>;
        close(FILE);
        $totalthreadcount = @allthreads;
        $count = 0;
        foreach $line (@allthreads) { #start foreach @threads
            ($tempno, $trash) = split(/\|/, $line);
            chomp $line;
            push (@numbercounter, $tempno);
            if ($intopic eq $tempno) {
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$line);
                $threadviews++; $keepcounter = $count;
                $linetokeep = "$topicid|$topictitle|$topicdescription|$threadstate|$threadposts|$threadviews|$startedby|$startedpostdate|$lastposter|$lastpostdate";
                chomp $linetokeep;
                $processed_data .= "$linetokeep\n";
                }
                else { $processed_data .= "$line\n"; }
            $count++;
            }
        if (($processed_data eq "") || ($processed_data !~ m!\|!)) { &error("Missing Data&Data as corrupted on the server. Please go back and try again"); }
        open(FILE, ">$filetoopen");
          flock(FILE, 2);
        print FILE $processed_data;
        close(FILE);
        undef $processed_data;
        my $file = "$ikondir" . "forum$inforum/$intopic.pl";
        open(MSG, ">$file");
        flock(MSG, 2);
        print MSG $linetokeep;
        close(MSG);
        }    
            
    $totalthreadcount = @numbercounter; $totalthreadcount--;

    if ($intopic eq $numbercounter[0]) { undef $nextlink; }
        else {
            $nexttopic = $keepcounter - 1;
            $threadnext = $numbercounter[$nexttopic];
            $nextlink = qq~<a href="$threadprog?forum=$inforum&topic=$threadnext"> $ibtxt{'3003'} >></a>~;
            }
        
    if ($intopic eq $numbercounter[$totalthreadcount]) { undef $backlink; }
        else {
            $backtopic = $keepcounter + 1;
            $threadback = $numbercounter[$backtopic];
            $backlink = qq~<a href="$threadprog?forum=$inforum&topic=$threadback"><< $ibtxt{'3004'} </a>~;
            }
        
    $nexttopiclinks = "$ibtxt{'3019'}<br>"; $nexttopiclinks .= "$backlink" if $backlink; $nexttopiclinks .= "$nextlink" if $nextlink;
        
    &postings;
    &whosonline("$inmembername|$ibtxt{'3020'} <a href=\"$threadprog?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a> $ibtxt{'2028'} <a href=\"$forumsprog?forum=$inforum\"><b>$forumname</b></a>|$ibtxt{'1602'}") if ($privateforum ne "yes");
    &moderator;
    &title;

    $filetoopen = "$ikondir" . "forum$inforum/$intopic.thd";
    $filetoopen = &stripMETA($filetoopen);
        if (-e $filetoopen) {
        open(FILE, $filetoopen) or &error("$ibtxt{'3005'}&$ibtxt{'3006'}");
        @threads = <FILE>;
        close(FILE);
        }
        else { 
          &error("$ibtxt{'3005'}&$ibtxt{'3006'}"); 
         }; 
    ($trash, $topictitle) = split(/\|/,$threads[0]);

    $numberofitems = @threads;
    $numberofpages = $numberofitems / $maxthreads;

    if ($numberofitems > $maxthreads) {
        $showmore = "yes";
        if ((!$instart) or ($instart < 0) or ($instart >= $numberofitems)) { $instart = 0; }
        if ($instart > 0) { $startarray = $instart; } else { $startarray = 0; }
        $endarray = $instart + $maxthreads - 1;
        if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
        if (($endarray > ($maxthreads - 1)) and ($more ne "yes")) { $endarray = $numberofitems - 1; }
        }
        else {
             $showmore = "no";
             $startarray = 0;
             $pages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1>$ibtxt{'3007'}</font>~;
             $endarray = $numberofitems - 1;
             }

     if ($showmore eq "yes") {
     if ($maxthreads < $numberofitems) {
        ($integer,$decimal) = split(/\./,$numberofpages);
        if ($decimal > 0) { $numberofpages = $integer + 1; }
            $pagestart = 0; $counter = 0;
            while ($numberofpages > $counter) {
                $counter++;
                if ($instart ne $pagestart) { $pages .= qq~<a href="$thisprog?forum=$inforum&topic=$intopic&start=$pagestart"><font face="$font" color=$fonthighlight size=$dfontsize1><b>$counter</b></font></a> ~; }
                else { $pages .= qq~<a href="$thisprog?forum=$inforum&topic=$intopic&start=$pagestart"><font face="$font" color=$menufontcolor size=$dfontsize1>$counter</font></a> ~; }
            $pagestart = $pagestart + $maxthreads;
            }
        }
     $pages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1><b>$ibtxt{'3008'}</b> [ $pages ]~;
     } 

    if (("$privateforum" eq "yes" && "$allowed" ne "yes")) { &error("$ibtxt{'1606'}&$ibtxt{'1607'}"); }
    $printpageicon = qq~<a href="$printpageprog?forum=$inforum&topic=$intopic"><img src="$imagesurl/images/$printpage" border=0></a>~;
    if ($privateforum ne "yes") { $sendtofriendicon = qq~<a href="$ikonfriendprog?forum=$inforum&topic=$intopic"><img src="$imagesurl/images/$emailtofriend" border=0></a>~; }

#------- HTML

        $output .= qq~
        <!-- Cgi-bot Start top of topic page -->
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
            <tr><td width=30% rowspan=2>$forumgraphic</td>
                    <td valign=middle align=top><font face="$font" color=$fontcolormisc size=$dfontsize2>
	                    &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	                    <br>
                        &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/closedfold.gif" border=0>&nbsp;&nbsp;<a href="$forumsprog?forum=$inforum">$forumname</a>
                        <br>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$topictitle</font>
                    </td>
                $uservisitdata
                </tr>
        </table>
        <br>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
        <table cellpadding=3 cellspacing=1 border=0 width=100%>
            <tr bgcolor="$menubackground"><td valign=middle align=center nowrap width=10%><font face="$font" color=$fontcolormisc size=$dfontsize1>
                $nexttopiclinks</td><td width=100%>$pages<br><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'0604'}</b> $modoutput
                </td>
                <td align=right valign=bottom bgcolor=$menubackground nowrap>$sendtofriendicon&nbsp;$printpageicon
                </td>
                </tr>
            </table>
        </td></tr></table>
        <p>
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
                <table cellpadding=3 cellspacing=1 border=0 width=100%>
                <tr>
                <td bgcolor=$titlecolor colspan=2 align="left" valign="middle">$newthreadbutton &nbsp; $replybutton</td>
            </tr>
         <!-- Cgi-bot End top of topic page -->
         ~;

#------- END HTML

    $editpostnumber = $startarray; $editpostnumber++; $postcountnumber = 0;
     
    foreach (@threads[$startarray .. $endarray]) {

        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\|/,$_);
        
        $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
        $postdate = &dateformat("$postdate");
    
        &gettopicmember("$membername");
        #^Именно эту подпрограмму надо вызывать
        $mname=$membername; 
        $m_membername = $membername;
        $m_membername =~ y! !_!; &set_up_guest() unless (-e $ikondir . 'members/'.$m_membername.'.cgi');
        
        if ($membername eq "$ibtxt{'0043'}") { $joineddate = "Never"; }
		elsif ($joineddate) {
            $joineddate = $joineddate + ($timedifferencevalue*3600) + ($timezone*3600);
            $joineddate = &joineddate("$joineddate");
            }
            else { $joineddate = "$ibtxt{'3009'}"; }

        if (!$numberofposts) { $numberofposts = "$ibtxt{'3009'}"; }
        if ($membername eq "$ibtxt{'0043'}") { $numberofposts = "$ibtxt{'3009'}"; }
    
        if (($post =~ /#Moderation Mode/i) and ($membercode eq 'mo' || $membercode eq 'ad')) {
            $post =~ s/&lt;/</g; $post =~ s/&gt;/>/g; $post =~ s/&quot;/\"/g;
            }

         if ($htmlstate eq 'on') {
            $post =~ s/&lt;/</g; $post =~ s/&gt;/>/g; $post =~ s/&quot;/\"/g;
            }
            
        if ($idmbcodestate eq 'on') {
            $post = &ikoncode("$post");
            }
        
        if ($count eq 1) {
                $postbackcolor = "$postcolorone"; $postfontcolor = "$postfontcolorone"; $count++;
                }
                else {
                    $postbackcolor = "$postcolortwo"; $postfontcolor = "$postfontcolortwo"; $count = 1;
                    }
    
        if (($emoticons eq 'on') and ($showemoticons eq 'yes') and ($post =~ /:(.+?):/)) {
            $post = &doemoticons("$post");
            }
    
        if (($emoticons eq 'on') && ($showemoticons eq 'yes')) {
            $post =~ s/\:\)/<img src=\"$imagesurl\/emoticons\/smile.gif\" border=\"0\">/g;
            $post =~ s/\;\)/<img src=\"$imagesurl\/emoticons\/wink.gif\" border=\"0\">/g;
            $post =~ s/\:\(/<img src=\"$imagesurl\/emoticons\/sad.gif\" border=\"0\">/g;
            $post =~ s/\:o/<img src=\"$imagesurl\/emoticons\/shocked.gif\" border=\"0\">/g;
            }
            
        
        if (($signature) and ($showsignature eq 'yes')) {
            $signature =~ s/</&lt;/g; $signature =~ s/>/&gt;/g;
            $signature =~ s/\&amp;/\&/isg;
            $signature =~ s/\[b\]/<b>/isg;
            $signature =~ s/\[\/b\]/<\/b>/isg;
            $signature =~ s/\[i\]/<i>/isg;
            $signature =~ s/\[\/i\]/<\/i>/isg;
            $signature =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=\"$1\" target=\"_blank\">$2<\/a>/isg; 
            $signature =~ s/\[url\]\s*http:\/\/(.*?)\s*\[\/url\]/<a href=\"http:\/\/$1\" target=\"_blank\">http:\/\/$1<\/a>/isg;
            $signature =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=\"http:\/\/$1\" target=\"_blank\">$1<\/a>/isg;
            $signature =~ s/\[br\]/\<br\>/isg;
            $signature =~ s/\\(\S+?)\@(\S+)/<a href="mailto:$1\@$2\"\>$1\@$2<\/a>/ig;             	    
            $signature =~ s/\[email=(\S+?)\]/<a href=\"mailto:$1\">/isg;             	    
            $signature =~ s/\[\/email\]/<\/a>/isg;
            $post = qq($post<br><br>-----<br>$signature);
            }
            
        if    ($numberofposts > $mpostmark5) { $mtitle = "$mtitle5";  $membergraphic = "$mgraphic5"; }
        elsif ($numberofposts > $mpostmark4) { $mtitle = "$mtitle4";  $membergraphic = "$mgraphic4"; }
        elsif ($numberofposts > $mpostmark3) { $mtitle = "$mtitle3";  $membergraphic = "$mgraphic3"; }
        elsif ($numberofposts > $mpostmark2) { $mtitle = "$mtitle2";  $membergraphic = "$mgraphic2"; }
        else { $mtitle = "$mtitle1"; $membergraphic = "$mgraphic1"; }
        
      if (($pips eq 'on') && ($membergraphic)) { $membergraphic = "<img src=\"$imagesurl/images/$membergraphic\" border=\"0\">"; }
      else { undef $membergraphic;}
        
        if (($avatars eq "on") && ($useravatar) && ($useravatar ne "noavatar")) {
            $useravatar = qq(<br><img src="$imagesurl/avatars/$useravatar.gif" border=0 width="32" height="32">);
            }
            else { undef $useravatar; }


        $memberfilename = $membername;
        $memberfilename =~ y/ /_/;
        
        if ($threadstate ne "closed") { 
           if ($text_menu ne "yes"){$replygraphic = qq~<a href="$postprog?action=replyquote&forum=$inforum&topic=$intopic&postno=$editpostnumber"><img src="$imagesurl/images/$reply" border=0></a>~;}
           else{$replygraphic = qq~| <a href="$postprog?action=replyquote&forum=$inforum&topic=$intopic&postno=$editpostnumber">Цитата</a>~;} 
            }
            else {
                 undef $replygraphic;
                }
        if ($text_menu ne "yes"){        
            $privatemessagegraphic = qq~<a href="javascript:openScript('$messengerprog?action=new&touser=$memberfilename',600,400)"><img src="$imagesurl/images/$message" border=0></a>~;
         
            $profilegraphic = qq~<a href="$profileprog?action=show&member=$memberfilename"><img src="$imagesurl/images/$profile" border=0></a>~;
            $editgraphic    = qq~<a href="$postingsprog?action=edit&forum=$inforum&topic=$intopic&postno=$editpostnumber"><img src="$imagesurl/images/$edit" border=0></a>~;
            $partition      = qq~<img src="$imagesurl/images/$part" border=0>~;
        } else  {
            
            $privatemessagegraphic = qq~ | <a href="javascript:openScript('$messengerprog?action=new&touser=$memberfilename',600,400)">Сообщение</a>~;
            $profilegraphic = qq~ | <a href="$profileprog?action=show&member=$memberfilename">Профиль</a>~;
            $editgraphic    = qq~<a href="$postingsprog?action=edit&forum=$inforum&topic=$intopic&postno=$editpostnumber">Правка</a>~;
          }   
            
    
        if($showemail eq "yes") { 
           if ($text_menu ne "yes"){   
              $emailgraphic = qq~<a href="mailto:$emailaddress"><img src="$imagesurl/images/$email" border=0></a>~; }
           else {$emailgraphic = qq~ | <a href="mailto:$emailaddress">E-mail</a>~; }
        }      
        else { undef $emailgraphic; }
    
        $homepage =~ s/http\:\/\///sg;
        if($homepage) { 
           if ($text_menu ne "yes"){   
              $homepagegraphic = qq~<a href="http://$homepage" target="_blank"><img src="$imagesurl/images/$homepagepic" border=0></a>~; }
           else {$homepagegraphic = qq~ | <a href="http://$homepage" target="_blank">WWW</a>~; }
        }
        else { undef $homepagegraphic; }
        
        
        if ($aolname) { 
            if ($text_menu ne "yes"){   
              $aolgraphic = qq~<a href="javascript:openScript('$miscprog?action=aim&aimname=$aolname',450,200)"><img src="$imagesurl/images/$aol" border=0></a>~; }
           else {
            $aolgraphic = qq~ | <a href="javascript:openScript('$miscprog?action=aim&aimname=$aolname',450,200)">AOL</a>~; }
        }    
         else { undef $aolgraphic; }
    
        if (($icqnumber) && ($icqnumber =~ /[0-9]/)) {
            if ($text_menu ne "yes"){   
              $icqgraphic = qq~<a href="javascript:openScript('$miscprog?action=icq&UIN=$icqnumber',450,300)"><img src="http://wwp.icq.com/scripts/online.dll?icq=$icqnumber&img=5" border=0><img src="$imagesurl/images/$icq" border=0></a>~;  }
           else {
            $icqgraphic = qq~ | <a href="javascript:openScript('$miscprog?action=icq&UIN=$icqnumber',450,300)">ICQ</a>~; }
         }
         else { undef $icqgraphic; }
    
     
        if ($membercode eq "ad") {
            $posterfontcolor = "$adminnamecolor";
            if ($team){
            $membername = "$membername <img src=\"$imagesurl/images/$team\" border=0>";}
          if ($pips eq 'on'){
            $membergraphic = "<img src=\"$imagesurl/images/$admingraphic\" border=\"0\">";}
            else { undef $membergraphic;}
            if ($membertitle eq "") { $membertitle = "$ibtxt{'1874'}"; }
            }
            elsif ($membercode eq "mo") {
                   $posterfontcolor = "$teamnamecolor";
                   $membername = "$membername <img src=\"$imagesurl/images/team.gif\" border=0>";
                if ($membertitle eq "") { $membertitle = "$ibtxt{'0007'}"; }
                }
                elsif ($membercode eq "banned") {
                    $posterfontcolor = "$posternamecolor";
                    $membergraphic = "";
                    $membertitle = "$ibtxt{'3010'}";
                    }
                    else { $posterfontcolor = "$posternamecolor"; }
                    
    
     if ($locations_in_topic eq 'on') {
            if ($location){
            
            if (length($location) > $char_locat_in_topic) {
            $location = substr($location, 0, $char_locat_in_topic-1);
            $location .= ' ...';
            }

            $locat = qq~<br>Откуда: $location<p>~;
            }
            else {undef $locat;}            
            } 
        
    $membertitle =~ s/&lt;/</g; $membertitle =~ s/&gt;/>/g; $membertitle =~ s/&quot;/"/g;

    $post =~ s/\($ibtxt{'1537'}(.+?)\)/\<font size=$dfontsize1>\($ibtxt{'1537'}$1\)\<\/font\>/isg;
    
    $post = &Truncate("$post");
    
    if ($iplog eq 'lnk'){$view_ip = qq~ | <a href="$viewipprog?forum=$inforum&topic=$intopic&postno=$editpostnumber">$ibtxt{'3013'}</a>~;}
    elsif ($iplog eq 'on'){$view_ip = qq~ | $postipaddress~;}
    else {undef $view_ip;}
    
#------- HTML
    
    $output .= qq~
    <!--Begin Msg Number $postcountnumber-->
		<tr>
			<td bgcolor="$postbackcolor">
			<table width=100% cellpadding=4 cellspacing=0 bgcolor="$postbackcolor">
			<tr>
        		<td bgcolor="$postbackcolor" valign="top" width=20%  rowspan=2>
            		<font face="$posternamefont" color="$posterfontcolor" size="$dfontsize2">
            		<a href="javascript:paste('$mname')"><b>$membername</b></a></font> 
            		<br>$useravatar
            		<br>$membergraphic
            		<br><font face="$font" color=$postfontcolor size=$dfontsize1>$membertitle $locat</font>
            		
        		</td>
        		<td bgcolor="$postbackcolor" valign=top width=80% height=100%><font face="$font" color=$postfontcolor size=$dfontsize1>
            		$editgraphic $partition $profilegraphic $homepagegraphic $emailgraphic $privatemessagegraphic $aolgraphic $icqgraphic $partition $replygraphic
    			    </font><hr size=1 width=100% color=$tablebordercolor>
            		<font face="$font" color=$postfontcolor size=$dfontsize2>
           			$post
				</td>
			</tr>
			<tr>
				<td class="bottomline" bgcolor="$postbackcolor">
					<hr size=1 width=100% color=$tablebordercolor>
                    <font face="$font" color=$postfontcolor size=$dfontsize1>$ibtxt{'0212'} <b>$numberofposts</b> | $ibtxt{'3012'} <b>$joineddate</b> | $ibtxt{'0319'}: <b>$postdate</b>$view_ip</font>
    		    </td>
             </tr>
			</table>
			</td>
		</tr>
    <!-- end Message -->
    ~;

#------- END HTML

    $editpostnumber++; $postcountnumber++; undef $membercode;

    }

#------- HTML

    $output .= qq~
    <!-- Cgi-bot Bottom of page -->
        <tr>
            <td bgcolor=$titlecolor colspan=2 align="left" valign="middle">$newthreadbutton &nbsp; $replybutton</td>
            </tr>
            </table>
        </td>
      </tr>
    </table>
    <p>
    ~;
 #################################### Форма ответа #########################     

    &getforum("$inforum");

        if ($allowedentry{$inforum} eq "yes") { $allowed = "yes"; }
        
        if (($privateforum eq "yes") && ($allowed ne "yes")) {
            &error("$ibtxt{'1406'}&$ibtxt{'1407'}");
        }   

    if ($threadstate ne "closed" && $threadstate ne 'moved'){


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

                
    $output .= qq~
    
     <SCRIPT language=Javascript> 
function paste(name){ 
var input=document.mt.elements[7]; 
input.value=input.value+"[b]"+name+"[/b]$rt"; 
} 
function paste2(name){ 
var input=document.mt.elements[7] 
if (name!="") input.value=input.value+"[quote]"+name+"[/quote]$rt" 
} 
</SCRIPT> 
    
    
        <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center> 
       <tr><td> 
           <table cellpadding=4 cellspacing=1 border=0 width=100%> 
               <tr> 
                   <td bgcolor=$postbackcolor colspan=2><font face="$font" color=$titlefontcolor size=0><b>Topic:</b> $topictitle</td> 
               </tr> 
               <tr><form name=mt action="$postprog" method=post> 
                   <input type=hidden name="action" value="addreply"> 
                   <input type=hidden name="forum" value="$inforum"> 
                   <input type=hidden name="topic" value="$intopic"> 
                   <input type=hidden name="previewfirst" value="no"> 
                   <input type=hidden name="" value=""> 
               </tr><tr> 
                   <td bgcolor=$postbackcolor valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'0727'}</b></font></td> 
                   <td bgcolor=$miscbackone valign=middle><input type=text size=20 name="membername" value="$inmembername"><font face="$font" color=$fontcolormisc size=1> &nbsp; <a href="$registerprog">$ibtxt{'1417'}</a></font></td> 
               </tr><tr> 
                   <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'0728'}</b></font></td> 
                   <td bgcolor=$miscbackone valign=middle><input type=password size=20 name="password" value="$inpassword"> 
                   <font face="$font" color=$fontcolormisc size=1> &nbsp; <a href="$profileprog?action=lostpass">$ibtxt{'2411'}</a></font></td> 
               </tr><tr> 
                   <td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1421'}</b><br> 
               <br> 
               <A href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">Поддержка кодов смайликов включена</A><br><br>Для вставки имени, кликните на нем.<br> 
<SCRIPT language=JavaScript> 
if (navigator.appVersion.indexOf("MSIE")!= -1) document.writeln("Для вставки цитаты, выделите её и <a href='VBScript:paste2(document.selection.createRange().Text)'>нажмите эту ссылку</a><br></span>") 
</SCRIPT></font> 
</td> 

                  <td bgcolor=$miscbackone valign=middle><textarea cols=60 rows=6 wrap="soft" name="inpost">$inpost</textarea> 
</td> 
               </tr><tr> 
                   <td bgcolor=$miscbacktwo valign=top><font face="$font" color=$fontcolormisc size=1><b>$ibtxt{'1425'}</b><p>$helpurl</font></td> 
                   <td bgcolor=$miscbacktwo valign=middle><font face="$font" color=$fontcolormisc size=1><input type=checkbox name="inshowsignature" value="yes" checked>$ibtxt{'1426'}<br> 
                   $requestnotify 
                   $emoticonsbutton 

                   </font></td> 
               </tr><tr> 
                   <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
                   <input type=Submit value=$ibtxt{'0039'} name="Submit" onClick="return clckcntr();"> &nbsp; <input type="reset" name="Clear"></form> 
               </td></tr> 
           </table></td></tr> 
       </table> 
       <p>
                    ~;
                    
}                    
 # #################################### Форма ответа #########################    
     $output .= qq~  
    
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
        <td>
        <table cellpadding=3 cellspacing=1 border=0 width=100%>
            <tr bgcolor="$menubackground"><td valign=middle align=center nowrap width=10%><font face="$font" color=$fontcolormisc size=$dfontsize1>
            $nexttopiclinks</td>
            <td valign=middle nowrap width=30%>
            <font face="$font" color=$menufontcolor size=$dfontsize1>$pages</td>
            <td align=right valign=bottom bgcolor=$menubackground nowrap>$jumphtml</td>
        </tr>
        </table></td></tr></table>
        <p>
        ~;
	&getmember($inmembername);
	if ($membercode eq "ad" || $membercode eq "mo") { 
	$output .= qq~
        <table cellspacing=3 cellpadding=0 width=$tablewidth align=center>
        <tr><td>
        <td valign=middle nowrap align=right><font face="$font" color=$menufontcolor size=$dfontsize1>
            $ibtxt{'3014'} <a href="$postingsprog?action=lock&forum=$inforum&topic=$intopic">$ibtxt{'3015'}</a> | 
            <a href="$postingsprog?action=edittopic&forum=$inforum&topic=$intopic">$ibtxt{'9999'}</a> | 
            <a href="$postingsprog?action=unlock&forum=$inforum&topic=$intopic">$ibtxt{'3016'}</a> | 
            <a href="$postingsprog?action=delete&forum=$inforum&topic=$intopic">$ibtxt{'3017'}</a> | 
            <a href="$postingsprog?action=movetopic&forum=$inforum&topic=$intopic">$ibtxt{'3018'}</a>
        </td>
    </tr>
    </table>
    <p>
    <p>
    <!-- Cgi-bot End bottom page -->
    ~;
      }
#------- END HTML

# Номер страницы на многостраничных темах Shurik & DimoN
if ($numberofitems > $maxthreads) {
if ($instart == 0) {$pagenumber = 1;}
else {$pagenumber = ($instart/$maxthreads)+1;}

    &output(
        -Title   => "$boardname - $topictitle - [$pagenumber]", 
        -ToPrint => $output, 
        -Version => $versionnumber 
        );
} else {

    &output(
        -Title   => "$boardname - $topictitle", 
        -ToPrint => $output, 
        -Version => $versionnumber 
        );
}

sub postings {

$newthreadbutton = qq~<a href="$postprog?action=new&forum=$inforum"><img src="$imagesurl/images/$newthread" border="0"></a>~;

if ($threadstate ne "closed") {
    $replybutton = qq~<a href="$postprog?action=reply&forum=$inforum&topic=$intopic"><img src="$imagesurl/images/$replytothread" border="0"></a>~;
    }
    else { $replybutton = qq~<img src="$imagesurl/images/$closed" border="0">~; }
}


#------- END OF SCRIPT
