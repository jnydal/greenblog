/*
* 
* nifrost-band site client class
*
*/
var GREENBLOG = {
		currentView: null,
		currentNewsPageNumber : 0,
		serversalt : '',
		user: null,
		challenge : '',
		isLastNewsPage : false,
		init:function() {
			
			this.loadWSYG();
			this.initFunctionalStyles();
			this.initLazyPostLoading();
			
		},
		initLazyPostLoading:function() {
			$(window).scroll(function(){
			     if  (($(window).scrollTop() == $(document).height() - $(window).height())&&(!GREENBLOG.isLastNewsPage)&&(GREENBLOG.currentView == "newsView")) {
			        GREENBLOG.ajaxLoadLastNewsPage();
			     }
			}); 
		},
		getNextNewsPageNumber:function() {
			var result = this.currentNewsPageNumber+"";
			this.currentNewsPageNumber++;
			return result;
		},
		resetCurrentNewsPage:function() {
			this.currentNewsPageNumber = 0;
			this.isLastNewsPage = false;
		},
		insertHashedPassword:function(form_id_string,withChallenge) {
			
			var unencrypted_password = $('#' + form_id_string + ' > #password').val();
			var salted_encrypted_password = hex_hmac_sha1(unencrypted_password,GREENBLOG.seversalt);
			var passwordhash = "";
		
			if (withChallenge==true) {
			
				passwordhash = hex_sha1(salted_encrypted_password+""+this.challenge);
						
			}else {
			
				passwordhash = salted_encrypted_password;
			
			}
			
			$('#' + form_id_string + ' > #password').val(passwordhash);
			
		},
		loadWSYG:function() {
		    $("#elm1").cleditor();
		},
		initFunctionalStyles:function() {

        	$("input").addClass("idle");
        	$("input").focus(function(){
           	 $(this).addClass("activeField").removeClass("idle");
	    	}).blur(function(){
	       	     $(this).removeClass("activeField").addClass("idle");
			});

		},
		ajaxLoadPage:function(key_name) {
		
			$("#main_content").empty();
			$('div#ajaxLoader').show();
			
			jQuery.ajax({
			    type: "GET",
			    url: "/rest/page/"+key_name+"/",
			    dataType: "json",
			    success: function(data){
			    	var admin_links = '';
			    	if (GREENBLOG.user != null) admin_links = '<div class="admin_options"><a href="/edit/page/'+key_name+'/" id="p_'+key_name+'"><img title="edit page..."  alt="edit page..." src="/static/images/edit-32.png"/></a><a href="/delete/page/'+key_name+'/" class="delete_page_link" id="p_'+key_name+'"><img title="delete page..." src="/static/images/cross.png"/></a></div';
			        var page = data[0].content + '<div class="date_field">'+ data[0].updated + '</div>';
			        $('#main_content').html(admin_links+page);
			    },
			    error: function(XMLHttpRequest, textStatus, errorThrown){
			        $('#main_content').html('<h2>404 page not found.</h2>');
			    },
			    complete: function() {
			    	$('div#ajaxLoader').fadeOut();
			    }
			});
			
			GREENBLOG.currentView = "pageView";
			
		},
		ajaxLoadLastNewsPage:function()	{
		    
		    $('div#ajaxLoader').show();
		    
		    var pageToLoad = GREENBLOG.getNextNewsPageNumber();
		    
		    jQuery.ajax({
			    type: "GET",
			    url: "/rest/news/"+pageToLoad+"/",
			    dataType: "json",
			    success: function(newspage){
				    $.each(newspage, function(i,post){
				    	var admin_links = "";
				    	if (GREENBLOG.user != null) admin_links = '<div class="admin_options"><a href="/edit/post/'+post.id+'/" id="p_'+post.id+'"><img title="edit post..."  alt="edit post..." src="/static/images/edit-32.png"/></a><a href="/delete/post/'+post.id+'/" class="delete_post_link" id="p_'+post.id+'"><img title="delete post..." src="/static/images/cross.png"/></a></div';
			            var post = '<h2>'+post.title + '</h2><div class="post_content">' + post.content + '</div><div class="date_field">' + post.created + '</div>';
			            $('#main_content').append(admin_links+post);
			        });
			        $('div#ajaxLoader').fadeOut();
			    },
			    error: function(XMLHttpRequest, textStatus, errorThrown){
			    	$('div#ajaxLoader').fadeOut();
			    	GREENBLOG.isLastNewsPage = true;
			    }
			});
			
			GREENBLOG.currentView = "newsView";
		    
		}
		
};