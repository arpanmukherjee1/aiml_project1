
// https://stackoverflow.com/questions/19447435/ajax-upload-image

$('#uplForm').on('submit', function(e){
	
	e.preventDefault();		
	// var form_data = new FormData(this);	
	f = $('#upl')[0].files[0]
	if(!f){
		alert('Choose a file!!!');
		return;
	};
	$('#pred').prop('disabled', true);
	$('#predOutput').text('Thinking...');
	var form_data = new FormData();
	form_data.append('image', f);
	
	const searchMethod = $("input[type='radio'][name='options']:checked").val();
	const url = new URL(window.location.href);
	url.port = '8080'
	url.pathname = '/predict'
	url.searchParams.append('searchmethod', searchMethod)
		
	$.ajax({
        url : url, 
        type : 'POST',
        data : form_data,
		//body: form_data,
        processData: false,
        contentType: false,
        success : function(resp){
			$('#pred').prop('disabled', false);
			$('#predOutput').text(resp.prediction);
        },
		error: function(resp){
			$('#pred').prop('disabled', false);
			resText = 'ERROR !!';
			if(resp.readyState == 0 && resp.statusText == 'error'){
				resText = 'Backend API is not reachable. Try after sometime.';
			}			
			$('#predOutput').text(resText);
			console.error(resp);
		}
	});
});

originalPreviewSrc = null;

$('#upl').change(function(e){
	if(originalPreviewSrc == null){
		originalPreviewSrc = $('#preview').attr('src');
	};
	f = this.files[0];
	if(f){
		url = URL.createObjectURL(f);
		$('#preview').attr('src', url);
		$('#predOutput').text('');
	} else {
		$('#preview').attr('src', originalPreviewSrc);
	};
	
});