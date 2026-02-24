$(document).ready(function (){
    console.log('We are using JQuery');

    $('#btnRegister').click(function (event){
        event.preventDefault();
        console.log('Button Click');

        const stream_id = $('#stream_id').val();    // This field will get value when the user will click on the Edit button
        const stream_name = $('#stream_name').val();
        const stream_description = $('#stream_description').val();
        const stream_semester = $('#stream_semester').val();
        const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: stream_id ? `/stream/edit/${stream_id}/` : `/stream/add/`,
            method: 'POST',
            data: {
                stream_id: stream_id,
                stream_name: stream_name,
                stream_description: stream_description,
                stream_semester: stream_semester,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function(response){
                $("#stream_name").val("");
                $("#stream_description").val("");
                $("#stream_semester").val("");
                $('#btnRegister').text('Add');

                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(3000).fadeOut();

                $("#streamList").html(response.streams)
            },
            error: function(error) {
                const errorMsg = error.responseJSON?.message || "An error occur";
                $("#acknowledge").text(errorMsg)
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();

            }
        });
        
    });


    $(document).on('click', '.edit-btn', function(event){
        event.preventDefault();
        const stream_id = $(this).data('id');
        const stream_name = $(this).data('name');
        const stream_description = $(this).data('description');
        const stream_semester = $(this).data('semester')
        
        console.log(`Stream ID: ${stream_id} Stream Name: ${stream_name} Stream Description: ${stream_description} Stream Semester: ${stream_semester}`);

        $('#stream_id').val(stream_id);
        $('#stream_name').val(stream_name);
        $('#stream_description').val(stream_description);
        $('#stream_semester').val(stream_semester);
        $('#btnRegister').text('Update');
    });

    $(document).on('click', '.delete-btn', function(event){
        event.preventDefault();
        const stream_id = $(this).data('id');
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if(!confirm("Are you sure to delete this stream ?"))
            return;

        $.ajax({
            url:`/stream/delete/${stream_id}`,
            method:'POST',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response){
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut()
                
                $("#streamList").html(response.streams)
            },
            error: function(err) {
                $("#acknowledge").text("Failed to delete the stream")
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut()
            }
        });
    });
});