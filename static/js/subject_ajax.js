$(document).ready(function (){
    console.log('Subject Jquery..');
    // Create global variable for selected semester
    let selectedSemester = null;

    $(document).on('change', '#stream_id', function(event){
    // $('#stream_id').on('change', function () {
        const stream_id = $('#stream_id').val();
        console.log(`Stream selected:- ${stream_id}`);

        if(!stream_id){
            $('#stream_id').text('');
        }

        $.ajax({
            url: `/subject/get_total_sem/`,
            type: 'GET',
            data: {
                stream_id: stream_id,
            },
            success: function (response) {
                console.log(`Semester:- ${response.sem_data}`);

                let sem_dropdown = $('#subject_semester');
                sem_dropdown.empty();
                sem_dropdown.append(
                    '<option value="" selected disabled>Select Semester...</option>'
                );
                $.each(response.sem_data, function (index,sem) {
                    sem_dropdown.append(
                        `<option value="${sem}">Sem - ${sem}</option>`
                    );
                });

                // Apply selected semester AFTER dropdown populated
                if (selectedSemester) {
                    sem_dropdown.val(selectedSemester);
                    selectedSemester = null; // reset
                }
            },
            error: function () {
                console.log('Something went wrong')
            }
        });
    });

    $("#subject_register_btn").click(function (event){
        event.preventDefault();

        const subject_id = $("#subject_id").val();
        const stream_id = $("#stream_id").val();
        const subject_name = $("#subject_name").val();
        const subject_semester = $("#subject_semester").val();
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        console.log(stream_id, subject_name, subject_semester);

        $.ajax({
            url: subject_id ? `/subject/edit/${subject_id}/` : `/subject/add/`,
            method: 'POST',
            data: {
                subject_id: subject_id,
                stream_id: stream_id,
                subject_name: subject_name,
                subject_semester: subject_semester,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response){
                $("#stream_id").val("");
                $("#subject_id").val("");
                $("#subject_semester").val("");
                $("#subject_name").val("");
                
                $('#subject_register_btn').text('Add');
                $('#acknowledge').text(response.message)
                                .css('color','green')
                                .fadeIn().delay(2000).fadeOut();
                $('#subjectList').html(response.subjects);
            },
            error: function(error){
                const errorMessage = error.responseJSON?.message || 'An error occurred';
                $('#acknowledge').text(errorMessage)
                                .css('color','red')
                                .fadeIn().delay(2000).fadeOut();
            }
        });
    });

    $(document).on('click', '.sub-edit-btn', function(event){
        event.preventDefault();
        const subject_id = $(this).data('id');
        const stream_id = $(this).data('stream_id');
        const subject_name = $(this).data('subject_name');
        const subject_semester = $(this).data('subject_semester');
        
        selectedSemester = subject_semester;

        $('#stream_id').val(stream_id).trigger('change');

        console.log(`Subject ID: ${subject_id}, Subject Name: ${subject_name}, Subject Semester: ${subject_semester}`);

        $('#subject_id').val(subject_id);
        $('#stream_id').val(stream_id);
        $('#subject_semester').val(subject_semester);
        $('#subject_name').val(subject_name);
        $('#subject_register_btn').text('Update');
    });

    $(document).on('click', '.sub-delete-btn', function(event){
        event.preventDefault();
        const subject_id = $(this).data('id');
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if(!confirm("Are you sure to delete this Subject ?"))
            return;

        $.ajax({
            url:`/subject/delete/${subject_id}/`,
            method:'POST',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response){
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut()
                
                $("#subjectList").html(response.subjects)
            },
            error: function(err) {
                $("#acknowledge").text("Failed to delete the subject")
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut()
            }
        });
    });

});