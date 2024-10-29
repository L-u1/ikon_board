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
($0 =~ m,(.*)/[^/]+,)   && unshift (@INC, "$1");
($0 =~ m,(.*)\\[^\\]+,) && unshift (@INC, "$1");
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

$thisprog = "search.cgi";

$query = new CGI;

## Patched by Peter

for ('TYPE_OF_SEARCH','NAME_SEARCH','POST_SEARCH','FORUMS_TO_SEARCH','action','SEARCH_STRING','REFINE_SEARCH','CUR_TIME','nextforum','start') {
   next unless defined $_; 
   next if $_ eq 'SEND_MAIL'; 
   $tp = $query->param($_); 
   $tp = &unHTML("$tp"); 
   ${$_} = $tp; 
   } 

$ipaddress        = $ENV{'REMOTE_ADDR'};
$inmembername     = cookie("amembernamecookie");
$filename = $inmembername;

if (!$filename) {
    $filename = "$ibtxt{'0043'}$ipaddress";
    $filename =~ s/\.//g;
    }
    
$filename =~ y/ /_/;
$filename = "$filename" . "_sch.txt";

$searchfilename = "$ikondir" . "search/$filename";

$dirtoopen = "$ikondir" . "search";
opendir(DIR, "$dirtoopen");
while ($file = readdir(DIR)) {
	if ((stat("$dirtoopen/$file"))[9] < (time - 30*60)) {  
    unlink("$dirtoopen/$file");
	}
}
closedir(DIR);

print header('text/html; charset=windows-1251');

&title;

    $output .= qq~
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth align=center>
        <tr>
            <td width=30% rowspan=2>
            <img src="$imagesurl/images/$boardlogo" border=0>
            </td>
            <td valign=top align=left>
            <font face="$font" color=$fontcolormisc size=$dfontsize2>
	           &nbsp;&nbsp;<img src="$imagesurl/images/closedfold.gif" border=0><a href="$forumsummaryprog">&nbsp;&nbsp;$boardname</a>
	           <br>
            &nbsp;&nbsp;<img src="$imagesurl/images/bar.gif" border=0><img src="$imagesurl/images/openfold.gif" border=0>&nbsp;&nbsp;$ibtxt{'0119'}
            </td>
            </tr>
       </table>
    <p>
    <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=8 cellspacing=1 border=0 width=100%>
    ~;




# Do we have a search folder?

if (!-d "$dirtoopen") {
    mkdir("$dirtoopen", 0777) || &error("$ibtxt{'2001'}&$ibtxt{'2002'}");
    chmod(0777, "$dirtoopen");
    }

if ($action eq "startsearch") {

    $SEARCH_STRING =~ s/\, /\,/g;

    if ($TYPE_OF_SEARCH eq "username_search") {
        $REFINE_SEARCH = "$NAME_SEARCH";
        }
        else {
            $REFINE_SEARCH = "$POST_SEARCH";
            }
        

    open (SEARCH, ">$searchfilename") or die "$ibtxt{'2003'}";
    print SEARCH "$CUR_TIME\n";
    print SEARCH "$SEARCH_STRING\n";
    print SEARCH "$TYPE_OF_SEARCH\n";
    print SEARCH "$REFINE_SEARCH\n";
    print SEARCH "$FORUMS_TO_SEARCH\n";
    close (SEARCH);
    
    $relocurl = "$boardurl/$thisprog?action=continue";
        
        $output .= qq~
            <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=2><b>$ibtxt{'2001'}....</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=2>
            $ibtxt{'2004'}<br>
            <b>$ibtxt{'2005'}</b>
            <ul>
            <li>$ibtxt{'2006'}
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <meta http-equiv="refresh" content="2; url=$relocurl">
            ~;
            
    }

    elsif ($action eq "display") {
         &displayresults;
         }

    elsif ($action eq "continue") {

        &getmember($inmembername);

        # Grab the params

        open (INSEARCH, "$searchfilename");
        @searchparam = <INSEARCH>;
        close (INSEARCH);

        my $SEARCH_STRING    = $searchparam[1];
        chomp $SEARCH_STRING;
        my $TYPE_OF_SEARCH   = $searchparam[2];
        chomp $TYPE_OF_SEARCH;
        my $REFINE_SEARCH    = $searchparam[3];
        chomp $REFINE_SEARCH;
        my $FORUMS_TO_SEARCH = $searchparam[4];
        chomp $FORUMS_TO_SEARCH;

        
        @KEYWORDS = split(/\,/,$SEARCH_STRING);

        $filetoopen = "$ikondir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
          flock(FILE, 2);
        @forums = <FILE>;
        close(FILE);

        @checkforums = @forums;
        @checkforums = reverse(@checkforums);

        $search_in_forum = $FORUMS_TO_SEARCH;

        if ($FORUMS_TO_SEARCH eq "all") {
            $nextforum++;
            $search_in_forum = $nextforum;
            ($forumno, $trash) = split(/\|/,$checkforums[0]);
            
            if ("$search_in_forum" > "$forumno") { $nofile="true"; $FORUMS_TO_SEARCH = "done"; }
            }
            
       
        foreach $forum (@forums) { #start foreach @forums
            chomp $forum;
            ($tempforumno, $trash) = split(/\|/,$forum);
            if ($tempforumno eq $search_in_forum) { #1
                ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum) = split(/\|/,$forum);
                $nofile = "true" if (($privateforum eq "yes") && ($allowedentry{$forumid} ne "yes"));
                } #e1
               else { next; }   
            } # end foreach @allforums
            

            $filetoopen = "$ikondir" . "forum$forumid/list.cgi";
            open(FILE, "$filetoopen") or $nofile = "true";
              flock FILE, 1;
            @topics = <FILE>;
            close(FILE);

            if ($nofile ne "true") { #start nofile
            foreach $topic (@topics) { # start topic foreach
                chomp $topic;
                ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate) = split(/\|/,$topic);
        
                if ($TYPE_OF_SEARCH eq "keyword_search") {

                    if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") { #1
                        foreach (@KEYWORDS) { #new1
                            if (($topictitle =~ m|$_|gi)  and ("$lida" ne "$topicid")) { #2
                                $founditem = ("$forumid|$topicid|$topictitle|$topicdescription|$forumname|$startedpostdate|$ibtxt{'2043'} $_");
                                push (@founditems, $founditem);
                                $lida = $topicid;
                                } #e2
                             }
                        } #e1

                            if (($REFINE_SEARCH eq "both_search") or ($REFINE_SEARCH eq "post_search")) { # 1
                                $filetoopen = "$ikondir" . "forum$forumid/$topicid.thd";
                                open (THREAD, "$filetoopen") or next;
                                  flock THREAD, 1;
                                @thddata = <THREAD>;
                                close (THREAD);

                                foreach (@thddata) { # start foreach 'thd'
                                    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\|/,$_);
                                    foreach (@KEYWORDS) { #new1
                                    if (($post =~ m|$_|gi) and ("$lida" ne "$topicid")) { # s 'if' n1
                                        $founditem = ("$forumid|$topicid|$topictitle|$topicdescription|$forumname|$postdate|$ibtxt{'2043'} $_");
                                        push (@founditems, $founditem);
                                        $lida = $topicid;
                                        } # e 'if' n1
                                      }
                                    } # end foreach 'thd'
                            } # e1
                    } # END MAIN IF 'keyword_search'
                    
                    elsif ($TYPE_OF_SEARCH eq "username_search") {

                        if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") { #1
                            foreach (@KEYWORDS) { #new1
                            if (($startedby =~ m|$_|gi) and ("$lidc" ne "$topicid")) { #2
                                $founditem = ("$forumid|$topicid|$topictitle|$topicdescription|$forumname|$startedpostdate|Started by $_");
                                push (@founditems, $founditem);
                                $lidc = $topicid;
                                } #e2
                               }
                            } #e1

                                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "post_search") { # 1
                                    $filetoopen = "$ikondir" . "forum$forumid/$topicid.thd";
                                    open (THREAD, "$filetoopen") or next;
                                      flock THREAD, 1;
                                    @thddata = <THREAD>;
                                    close (THREAD);

                                    foreach (@thddata) { # start foreach 'thd'
                                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\|/,$_);
                                        foreach (@KEYWORDS) { #new1
                                        if (($membername =~ m|$_|gi) and ($lidc != $topicid)) { # s 'if' n1
                                            $founditem = ("$forumid|$topicid|$topictitle|$topicdescription|$forumname|$postdate|Posted in by $_");
                                            push (@founditems, $founditem);
                                            $lidc = $topicid;
                                            } # e 'if' n1
                                          }
                                        } # end foreach 'thd'
                                } # e1
                        } # END MAIN ELSIF 'username_search'
                    
                     } # end main foreach list loop

                    # What do we do next? First push all the data to the text file

                        $matches_in_forum = @founditems;
                        $matches_so_far   = @searchparam - 5;

                        open (OUT, ">>$searchfilename") or die "$ibtxt{'2003'}";
                        foreach (@founditems) {
                            chomp $_;
                            print OUT "$_\n";
                            }
                        close (OUT);
                    
                    undef @founditems;
                    undef @KEYWORDS;
                    } # end if no file
                    
                    # Then work out where to go

                    if ($FORUMS_TO_SEARCH eq "all") {
                        $relocurl = "$boardurl/$thisprog?action=continue&nextforum=$search_in_forum";
                        }
                        else {
                            $relocurl = "$boardurl/$thisprog?action=display";
                            }

                  $matches_in_forum = "$ibtxt{'2007'}" if (!$matches_in_forum);
                  $matches_so_far   = "$ibtxt{'2007'}" if (!$matches_so_far);
                  $forumname        = "$ibtxt{'2007'}" if (!$forumname);
      
          
                  $output .= qq~
			            <tr>
			            <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2001'}....</b></font></td></tr>
			            <tr>
			            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc size=$dfontsize2>
			            $ibtxt{'2004'}<br>
			            <b>$ibtxt{'2005'}</b>
			            <ul>
			            <li>$ibtxt{'2006'}
                        <li>$ibtxt{'2008'} <b>$forumname</b>
                        <li>$ibtxt{'2009'} - <b>$matches_so_far</b>
                        <li>$ibtxt{'2010'} $forumname - <b>$matches_in_forum</b>
			            </ul>
			            </tr>
			            </td>
			            </table></td></tr></table>
			            <meta http-equiv="refresh" content="2; url=$relocurl">
			            ~;

                  } # end if action eq continue


                    else {

                        # Print form

						&getmember("$inmembername");


						$jumphtml .= qq~
						<select name="FORUMS_TO_SEARCH">
						<option value="all">$ibtxt{'2011'}
						~;        

						$filetoopen = "$ikondir" . "data/allforums.cgi";
						open(FILE, "$filetoopen");
						  flock(FILE, 2);
						@forums = <FILE>;
						close(FILE);

						foreach $forum (@forums) { #start foreach @forums
						    chomp $forum;
						    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic) = split(/\|/,$forum);
						    if (($privateforum eq "yes") && ($userregistered ne "no") && ($allowedentry{$forumid} eq "yes")) {
						        $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forumid");
						        }
						        elsif ($privateforum ne "yes") {
						            $rearrange = ("$categoryplace|$category|$forumname|$forumdescription|$forumid");
						            }
						        push (@rearrangedforums, $rearrange);

						} # end foreach (@forums)

						@finalsortedforums = sort(@rearrangedforums);

						foreach $sortedforums (@finalsortedforums) { #start foreach 
						    ($categoryplace, $category, $forumname, $forumdescription, $forumid) = split(/\|/,$sortedforums);
						    
						    if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
						        $jumphtml .= "<option value=\"\">\n";
						        $jumphtml .= "<option value=\"\">-- &nbsp; $category\n";
						        $jumphtml .= "<option value=\"$forumid\"> $forumname\n";
						        }
						        else {
						            $jumphtml .= "<option value=\"$forumid\"> $forumname\n";
						            }
						     $lastcategoryplace = $categoryplace;
						     } # end foreach 
						     
						$jumphtml .= qq~</select>\n~;


						$refineposts = qq~<select name="POST_SEARCH">
						                  <option value="topictitle_search">$ibtxt{'2012'}
						                  <option value="post_search">$ibtxt{'2013'}
						                  <option value="both_search">$ibtxt{'2014'}
						                  </select>
						                  ~;

                        $refinename  = qq~<select name="NAME_SEARCH">
						                  <option value="topictitle_search">$ibtxt{'2015'}
						                  <option value="post_search">$ibtxt{'2016'}
						                  <option value="both_search">$ibtxt{'2017'}
						                  </select>
						                  ~;

                     $currenttime = time;
                        
						$output .= qq~
						<p><form action="$boardurl/$thisprog" method="post">
						<input type=hidden name="action" value="startsearch">
                     <input type=hidden name="CUR_TIME" value="$currenttime">
						<tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align="center"><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'2018'}</b></font></td></tr>
						<tr>
						<td bgcolor=$miscbackone width colspan=2 align="center" valign="middle"><font face="$font" color=$fontcolormisc size=$dfontsize2><b>$ibtxt{'2019'}</b>
						($ibtxt{'2024'} ',')</font><br><br><input type=text size=40 name="SEARCH_STRING"></td></tr>
                        <tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'2020'}</b></font></td></tr>
						
                        <tr>
						<td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc size=$dfontsize2>
                        <b>$ibtxt{'2021'}</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" value="username_search">
                        </td>
                        <td bgcolor="$miscbackone" align="left" valign="middle">
                        $refinename
                        </td>
                        </tr>
                        <tr>
                        <td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc size=$dfontsize2>
                        <b>$ibtxt{'2022'}</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" value="keyword_search" checked>
                        </td>
                        <td bgcolor="$miscbackone" align="left" valign="middle">
                        $refineposts
                        </td>
                        </tr>
                        <tr>
						<td bgcolor="$miscbacktwo" valign="middle" colspan=2 align=center><font face="$font" color=$fontcolormisc size=$dfontsize3><b>$ibtxt{'2023'}</b></font></td></tr>
						<tr>
						<td bgcolor="$miscbackone" colspan="2" valign="middle" align="center"><font face="$font" color=$fontcolormisc size=$dfontsize2>
                        <b>$ibtxt{'2042'} &nbsp; $jumphtml</b></td>
						</tr>
						<tr>
						<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center>
						<input type=submit value="$ibtxt{'0042'}">
						</form></td></tr></table></td></tr></table>
						~;
						}
                        &output(
	                    -Title   => "$boardname - $ibtxt{'0119'}", 
	                    -ToPrint => "$output", 
	                    -Version => $versionnumber 
	                    );

sub displayresults {

  

   open (READ, "$searchfilename") or &error("$ibtxt{'2025'}&$ibtxt{'2026'}");
   @completed_search = <READ>;
   close (READ);

   foreach (@completed_search) {
      push (@TRUE_RESULTS, $_) if ($_ =~ /\|/)
      }

   $total_results = @TRUE_RESULTS;

   $SEARCH_STRING    = $completed_search[1];
   chomp $SEARCH_STRING;
   $TYPE_OF_SEARCH   = $completed_search[2];
   chomp $TYPE_OF_SEARCH;
   $REFINE_SEARCH    = $completed_search[3];
   chomp $REFINE_SEARCH;
   $FORUMS_TO_SEARCH = $completed_search[4];
   chomp $FORUMS_TO_SEARCH;
   
   $TYPE_OF_SEARCH = "$ibtxt{'2037'}"  if ($TYPE_OF_SEARCH eq "keyword_search");
   $TYPE_OF_SEARCH = "$ibtxt{'2038'}"  if ($TYPE_OF_SEARCH eq "username_search");
	
   $REFINE_SEARCH = "$ibtxt{'2039'}" if ($REFINE_SEARCH eq "topictitle_search");
   $REFINE_SEARCH = "$ibtxt{'2040'}" if ($REFINE_SEARCH eq "post_search");
   $REFINE_SEARCH = "$ibtxt{'2041'}" if ($REFINE_SEARCH eq "both_search");

   if ($total_results > 0) {
      $result_line = qq($ibtxt{'2027'} <b>$TYPE_OF_SEARCH</b> $ibtxt{'2028'} <b>$REFINE_SEARCH</b> $ibtxt{'2029'} <b>$total_results</b> $ibtxt{'2030'});
      }
      else {
      		$result_line = qq($ibtxt{'2031'} <b>$TYPE_OF_SEARCH</b> $ibtxt{'2028'} <b>$REFINE_SEARCH</b> $ibtxt{'2044'});
          }	                  

						
   
   $output .= qq~
   <tr>
      <td bgcolor="$miscbacktwo" valign=middle colspan=3 align=center>
         <font face="$font" color=$fontcolormisc size=3>
         $result_line
         </font>
      </td>
   </tr>
   <tr>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc size=$dfontsize2>
         <b>$ibtxt{'0909'}</b></font>
      </td>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc size=$dfontsize2>
         <b>$ibtxt{'2032'}</b></font>
      </td>
      <td bgcolor=$miscbackone valign=middle align=center>
         <font face="$font" color=$fontcolormisc size=$dfontsize2>
         <b>$ibtxt{'2033'}</b></font>
         </font>
      </td>
   </tr>
   ~;
   ### Work out if there is a span, and if so how many pages.

    $maxthreads = 25;
    $numberofitems = $total_results;
    $numberofpages = $numberofitems / $maxthreads;
    $instart = $start;

    if ($numberofitems > $maxthreads) { #if
        $showmore = "yes";
        if ($instart eq "" || $instart < 0) { $instart = 0; }
        if ($instart > 0) { $startarray = $instart; }
            else { $startarray = 0; }
            $endarray = $instart + $maxthreads - 1;
            if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
            if (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $numberofitems - 1; }
            } #
            else {
                $showmore = "no";
                $startarray = 0;
                $pages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1>$ibtxt{'2034'}</font>~;
                $endarray = $numberofitems - 1;
                }

    ### if we have multiple pages, print them
    
        if ($showmore eq "yes") { #1
            if ($maxthreads < $numberofitems) { #2
                ($integer,$decimal) = split(/\./,$numberofpages);
                    if ($decimal > 0) { $numberofpages = $integer + 1; }
                        $pagestart = 0;
                        $counter = 0;
                            while ($numberofpages > $counter) { #3
                                $counter++;
                                if ($instart ne $pagestart) { $pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$fonthighlight size=1><b>$counter</b></font></a> ~; }
                                 else { $pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$menufontcolor size=1>$counter</font></a> ~; }
                                $pagestart = $pagestart + $maxthreads;
                                } #e3
                            } #e2
                $pages = qq~<font face="$font" color=$menufontcolor size=$dfontsize1><b>$ibtxt{'2035'}</b> [ $pages ]~;
                } #1

   foreach (@TRUE_RESULTS[$startarray .. $endarray]) { # start foreach loop

   ($forumid, $topicid, $topictitle, $topicdescription, $forumname, $postdate, $string_returned) = split(/\|/,$_);

   $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
   $longdate = &longdate("$postdate");

   $topicdescription = qq(&raquo; $topicdescription) if $topicdescription;
   
   $output .= qq(
   <tr>
      <td bgcolor=$miscbackone valign=middle>
         <font face="$font" color=$fontcolormisc size=$dfontsize2>
         <a href="$boardurl/$threadprog?forum=$forumid&topic=$topicid">$topictitle</a><br>
         <font size=$dfontsize1>$topicdescription
      </td>
      <td bgcolor=$miscbackone valign=middle>
         <font face="$font" color=$fontcolormisc size=$dfontsize1>
         $ibtxt{'0319'}: <b>$longdate</b> $ibtxt{'2028'} <a href="$boardurl/$forumsprog?forum=$forumid">$forumname</a></font>
      </td>
         <td bgcolor=$miscbackone valign=middle>
         <font face="$font" color=$fontcolormisc size=$dfontsize1>
         <b>$string_returned</b>
         </font>
      </td>
   </tr>
   );

   undef $topicdescription;

   } # end foreach

   $output .= qq(
      <tr>
      <td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center>
         <font face="$font" color=$fontcolormisc size=$dfontsize2>
         $pages
         </font>
      </td>
      <td bgcolor="$miscbacktwo" valign=middle colspan=1 align=center>
         <font face="$font" color=$fontcolormisc size=$dfontsize3>
         <a href="$boardurl/$thisprog"><b>$ibtxt{'2036'}</b></a>
         </font>
      </td>
   </tr>
   </table></td></tr></table>);


   &output( -Title   => "$boardname - $ibtxt{'2025'}", 
             -ToPrint => "$output", 
             -Version => $versionnumber);


} # end routine








