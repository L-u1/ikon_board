function thelp(swtch){
	if (swtch == 1){
		basic = false;
		stprompt = false;
		helpstat = true;
	} else if (swtch == 0) {
		helpstat = false;
		stprompt = false;
		basic = true;
	} else if (swtch == 2) {
		helpstat = false;
		basic = false;
		stprompt = true;
	} else {
		helpstat = false;
		basic = false;
		stprompt = false;
	}
}

function AddText(NewCode) {
document.PostTopic.inpost.value+=NewCode
}

function email() {
	if (helpstat) {
		alert("Email Tag\nTurns an email address into a mailto hyperlink.\nUSE: [email]emailadd[/email]\nUSE: [email=emailadd]link text[/email]");
	} else if (basic) {
		AddTxt="[email][/email]";
		AddText(AddTxt);
	} else { 
		txt2=prompt("Text to be shown for the link.\nLeave blank if you want the email address to be shown for the link.",""); 
		if (txt2!=null) {
			txt=prompt("Email address.","emailadd");      
			if (txt!=null) {
				if (txt2=="") {
					AddTxt="[email]"+txt+"[/email]";
				} else {
					AddTxt="[email="+txt+"]"+txt2+"[/email]";
				} 
				AddText(AddTxt);	        
			}
		}
	}
}

function showsize(size) {
	if (helpstat) {
		alert("Size Tag\nSets the text size.\nPossible values are 1 to 6.\n 1 being the smallest and 3 the largest.\nUSE: [size="+size+"]This is size "+size+" text[/size]");
	} else if (basic) {
		AddTxt="[size="+size+"][/size]";
		AddText(AddTxt);
	} else {                       
		txt=prompt("Text to be size "+size,"Text"); 
		if (txt!=null) {             
			AddTxt="[size="+size+"]"+txt+"[/size]";
			AddText(AddTxt);
		}        
	}
}

function showsize(size) {
	if (helpstat) {
		alert("Size Tag\nSets the text size.\nPossible values are 1 to 6.\n 1 being the smallest and 3 the largest.\nUSE: [size="+size+"]This is size "+size+" text[/size]");
	} else if (basic) {
		AddTxt="[size="+size+"][/size]";
		AddText(AddTxt);
	} else {                       
		txt=prompt("Text to be size "+size,"Text"); 
		if (txt!=null) {             
			AddTxt="[size="+size+"]"+txt+"[/size]";
			AddText(AddTxt);
		}        
	}
}

function bold() {
	if (helpstat) {
		alert("Bold Tag\nMakes the enlosed text bold.\nUSE: [b]This is some bold text[/b]");
	} else if (basic) {
		AddTxt="[b][/b]";
		AddText(AddTxt);
	} else {  
		txt=prompt("Text to be made BOLD.","Text");     
		if (txt!=null) {           
			AddTxt="[b]"+txt+"[/b]";
			AddText(AddTxt);
		}       
	}
}

function sound() {
	if (helpstat) {
		alert("Sound Tag\nInsert a sound into your post\nUSE: [sound]URL to sound[/sound]");
	} else if (basic) {
		AddTxt="[sound][/sound]";
		AddText(AddTxt);
	} else {  
		txt=prompt("URL to sound file.","http://");     
		if (txt!=null) {           
			AddTxt="[sound]"+txt+"[/sound]";
			AddText(AddTxt);
		}       
	}
}

function italicize() {
	if (helpstat) {
		alert("Italicize Tag\nMakes the enlosed text italicized.\nUSE: [i]This is some italicized text[/i]");
	} else if (basic) {
		AddTxt="[i][/i]";
		AddText(AddTxt);
	} else {   
		txt=prompt("Text to be italicized","Text");     
		if (txt!=null) {           
			AddTxt="[i]"+txt+"[/i]";
			AddText(AddTxt);
		}	        
	}
}

function quote() {
	if (helpstat){
		alert("Quote tag\nQuotes the enclosed text to reference something specific that someone has posted.\nUSE: [quote]This is a quote[/quote]");
	} else if (basic) {
		AddTxt="\r[quote]\r[/quote]";
		AddText(AddTxt);
	} else {   
		txt=prompt("Text to be quoted","Text");     
		if(txt!=null) {          
			AddTxt="\r[quote]\r"+txt+"\r[/quote]";
			AddText(AddTxt);
		}	        
	}
}

function showcolor(color) {
	if (helpstat) {
		alert("Color Tag\nSets the text color.  Any named color can be used.\nUSE: [color="+color+"]This is some "+color+" text[/color]");
	} else if (basic) {
		AddTxt="[color="+color+"][/color]";
		AddText(AddTxt);
	} else {  
     	txt=prompt("Text to be "+color,"Text");
		if(txt!=null) {
			AddTxt="[color="+color+"]"+txt+"[/color]";
			AddText(AddTxt);        
		} 
	}
}

function center() {
 	if (helpstat) {
		alert("Centered tag\nCenters the enclosed text.\nUSE: [center]This text is centered[/center]");
	} else if (basic) {
		AddTxt="[center][/center]";
		AddText(AddTxt);
	} else {  
		txt=prompt("Text to be centered","Text");     
		if (txt!=null) {          
			AddTxt="\r[center]"+txt+"[/center]";
			AddText(AddTxt);
		}	       
	}
}

function hyperlink() {
	if (helpstat) {
		alert("Hyperlink Tag\nTurns an url into a hyperlink.\nUSE: [url]http://www.anywhere.com[/url]\nUSE: [url=http://www.anywhere.com]link text[/url]");
	} else if (basic) {
		AddTxt="[url][/url]";
		AddText(AddTxt);
	} else { 
		txt2=prompt("Text to be shown for the link.\nLeave blank if you want the url to be shown for the link.",""); 
		if (txt2!=null) {
			txt=prompt("URL for the link.","http://");      
			if (txt!=null) {
				if (txt2=="") {
					AddTxt="[url]"+txt+"[/url]";
					AddText(AddTxt);
				} else {
					AddTxt="[url="+txt+"]"+txt2+"[/url]";
					AddText(AddTxt);
				}         
			} 
		}
	}
}

function image() {
	if (helpstat){
		alert("Image Tag\nInserts an image into the post.\nUSE: [img]http:\www.anywhere.comimage.gif[/img]");
	} else if (basic) {
		AddTxt="[img][/img]";
		AddText(AddTxt);
	} else {  
		txt=prompt("URL for graphic","http://");    
		if(txt!=null) {            
			AddTxt="\r[img]"+txt+"[/img]";
			AddText(AddTxt);
		}	
	}
}

function flash() {
	if (helpstat) {
		alert("Flash Tag\nInserts a flash movie into the post.\nUSE: [flash size=2]http://www.domain.com/flash.swf[/flash]\nUSE: [flash size=width,height]http://www.domain.com/flash.swf[/flash]");
	} else if (basic) {
		AddTxt="[flash size=2]http://[/flash]";
		AddText(AddTxt);
	} else { 
		txt2=prompt("Size of the flash movie (1, 2, 3).","2"); 
		if (txt2!=null) {
			txt=prompt("URL for the flash movie (.swf file).","http://");      
			if (txt!=null) {
				if (txt2=="") {
					AddTxt="[flash size=2]"+txt+"[/flash]";
					AddText(AddTxt);
				} else {
					AddTxt="[flash size="+txt2+"]"+txt+"[/flash]";
					AddText(AddTxt);
				}         
			} 
		}
	}
}

function showcode() {
	if (helpstat) {
		alert("Code Tag\nBlockquotes the text you reference and preserves the formatting.\nUsefull for posting code.\nUSE: [code]This is formated text[/code]");
	} else if (basic) {
		AddTxt="\r[code]\r[/code]";
		AddText(AddTxt);
	} else {   
		txt=prompt("Enter code","");     
		if (txt!=null) {          
			AddTxt="\r[code]"+txt+"[/code]";
			AddText(AddTxt);
		}	       
	}
}

function list() {
	if (helpstat) {
		alert("List Tag\nBuilds a bulleted, numbered, or alphabetical list.\nUSE: [list]\n[*]item1\n[*]item2\n[*]item3\n[/list]");
	} else if (basic) {
		AddTxt="\r[list]\r[*]\r[*]\r[*]\r[/list]";
		AddText(AddTxt);
	} else {  
		txt=prompt("Type of list\nEnter 'A' for alphabetical, '1' for numbered, Leave blank for bulleted.","");               
		while ((txt!="") && (txt!="A") && (txt!="a") && (txt!="1") && (txt!=null)) {
			txt=prompt("ERROR!\nThe only possible values for type of list are blank 'A' and '1'.","");               
		}
		if (txt!=null) {
			if (txt=="") {
				AddTxt="\r[list]\r\n";
			} else {
				AddTxt="\r[list="+txt+"]\r";
			} 
			txt="1";
			while ((txt!="") && (txt!=null)) {
				txt=prompt("List item\nLeave blank to end list",""); 
				if (txt!="") {             
					AddTxt+="[*]"+txt+"\r"; 
				}                   
			} 
			AddTxt+="[/list]\r\n";
			AddText(AddTxt); 
		}
	}
}

function underline() {
  	if (helpstat) {
		alert("Underline Tag\nUnderlines the enclosed text.\nUSE: [u]This text is underlined[/u]");
	} else if (basic) {
		AddTxt="[u][/u]";
		AddText(AddTxt);
	} else {  
		txt=prompt("Text to be Underlined.","Text");     
		if (txt!=null) {           
			AddTxt="[u]"+txt+"[/u]";
			AddText(AddTxt);
		}	        
	}
}

function showfont(font) {
 	if (helpstat){
		alert("Font Tag\nSets the font face for the enclosed text.\nUSE: [font="+font+"]The font of this text is "+font+"[/font]");
	} else if (basic) {
		AddTxt="[font="+font+"][/font]";
		AddText(AddTxt);
	} else {                  
		txt=prompt("Text to be in "+font,"Text");
		if (txt!=null) {             
			AddTxt="[font="+font+"]"+txt+"[/font]";
			AddText(AddTxt);
		}        
	}  
}
<!-- // cloak
var submitted = 0;
// -->
