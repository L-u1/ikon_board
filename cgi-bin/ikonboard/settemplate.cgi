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
require "ikon.lib";           # Require ikonboard ()
require "ikonadmin.lib";      # Require Admin func()
require "data/progs.cgi";     # Require prog names
require "data/boardinfo.cgi"; # Require board info
require "data/styles.cgi";    # Require styles info
require "data/boardstats.cgi";# Require styles info
};
if ($@) {
print header('text/html; charset=windows-1251'); print start_html(-title=>"$ibtxt{'0025'}");
    print "$ibtxt{'0026'} $@\n$ibtxt{'0027'}";
    print end_html; exit;
}

$|++;                                      # Unbuffer the output

#################--- Begin the program ---###################

$thisprog = "settemplate.cgi";

# sort out the incoming CGI

$query = new CGI;

&checkVALIDITY;

$cookiepath = $query->url(-absolute=>1);
$cookiepath =~ s/$thisprog//sg;

$process = $query ->param("process");
$action  = $query ->param("action");


$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");

if ($process ne "preview template") {
print header('text/html; charset=windows-1251');
   &admintitle;
   print qq(
   <tr><td bgcolor=#333333" ><font face=verdana size=3 color=#FFFFFF>
   <b>$ibtxt{'0208'}</b>
   </td></tr>);
   }

&getmember("$inmembername");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($inmembername eq $membername)) {

unless(defined($process)) {


   # Get the template file

   $templatefile = "$ikondir" . "data/template.dat";

   # Is it there?....

   if (-e $templatefile) {
      open (TEMPLATE, "$templatefile");
      local $/ = undef;
      $template_data = <TEMPLATE>;
      close (TEMPLATE);
      }
      else {
         print qq(<tr><td><font face="verdana" size="2" color="#FF0000">
                  <b>$ibtxt{'2301'}</b><br>
                  $ibtxt{'2302'}
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         } # end is it there

   # ....Is it writable?

   unless (-w $templatefile) {
         print qq(<tr><td><font face="verdana" size="2" color="#FF0000">
                  <b>$ibtxt{'2303'}</b><br><br>
                  $ibtxt{'2304'}<br>
                  $ibtxt{'2305'} 
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         }
      

   # If we're here, lets print out the template....

   ($non_editable, $user_editable) = split(/\<!--end Java-->/, $template_data);

   $non_editable =~ s/</&lt;/g;
   $non_editable =~ s/>/&gt;/g;
   $non_editable =~ s/\"/&quot;/g;
   
   $user_editable =~ s/</&lt;/g;
   $user_editable =~ s/>/&gt;/g;
   $user_editable =~ s/\"/&quot;/g;
   
   print qq(
   <tr>
   <td colspan=2>
   <form action="$thisprog" method=POST name="the_form">
   <input type="hidden" name="non_editable" value="$non_editable">
   <input type="hidden" name=process value="true">
   <textarea name="template_info" wrap="soft" cols="50" rows="20">
   $user_editable
   </textarea>
   <br><br>
   <input type="submit" value="$ibtxt{'2306'}" onclick="preview_template();">
   <input type="submit" value="$ibtxt{'2307'}" onclick="save_changes();">
   </form>
   <br><hr size=1 color=#000000>
   <font face="verdana" size="2" color="#000000">
   <b>$ibtxt{'2308'}</b><br>
   $ibtxt{'2309'}   
   <br>
   $ibtxt{'2310'} '\$ikonboard_main' $ibtxt{'2311'} '\$ikonboard_main' $ibtxt{'2312'}
   <br><br>
   $ibtxt{'2313'}
   <br>
   <b>$ibtxt{'2314'} &lt;/head&gt;,&lt;/body&gt; $ibtxt{'1854'} &lt;/html&gt; $ibtxt{'2315'}</b><br>
   $ibtxt{'2316'} &lt;html&gt; $ibtxt{'2317'}

   </td>
   </tr>
   );
   } # end if def(process)

   else {

      $template_info = $query -> param("template_info");
      $header_info   = $query -> param("non_editable");

      $header_info =~ s/&lt;/</g;
      $header_info =~ s/&gt;/>/g;
      $header_info =~ s/&quot;/\"/g;
   
      $template_info =~ s/&lt;/</g;
      $template_info =~ s/&gt;/>/g;
      $template_info =~ s/&quot;/\"/g;

      if ($process eq "preview template") {

print header('text/html; charset=windows-1251');

         &title;

         $temp_board = qq(
         <table width=$tablewidth border=1 align=center><tr><td>
         $output
         <br><br><br><br><br><br><br>
         <font face="verdana" color=#000000>
         <center><h1>$ibtxt{'2318'}</h1>
         $ibtxt{'2319'}
         <br><br></center>
         <font size=1>$ibtxt{'2320'}
         <br><br><br><br><br><br><br>
         <table width=80% align=center cellpadding=3 cellspacing=0>
         <tr><td align=center valign=middle>
         <font face=verdana color=#000000 size=1>
         $ibtxt{'1603'} <a href="http://www.ikonboard.com/ikonboard">Ikonboard $versionnumber</a><br>&copy; 2000 Ikonboard.com
         </font></td></tr></table>
         <p></td></tr></table></body></html>);

         $template_info =~ s/\$ikonboard_main/$temp_board\n/sg;

         print $header_info;
         print $template_info;

      }

      else {

         $templatefile = "$ikondir" . "data/template.dat";

         open (TEMPLATE, ">$templatefile") or die "$ibtxt{'0138'}";
           flock (TEMPLATE, 2);
         print TEMPLATE "$header_info\n";
         print TEMPLATE "<!--end Java-->\n";
         print TEMPLATE $template_info;
         close (TEMPLATE);

         
         print "<tr><td><font face=verdana size=2><b>$ibtxt{'2322'}</b></font></td></tr>";
         }

      }


   } # end if logged in

   else {
      &adminlogin;
      }
                

   print qq(</table></td></tr></table></td></tr></table></body></html>) if ($process ne "preview template");
   exit;
