$(document).on("click", ".open-MenuModal", function () {
  var name = $(this).data('id');
  $(".modal-body #name_id").val(name);
  // As pointed out in comments, 
  // it is unnecessary to have to manually call the modal.
  // $('#addBookDialog').modal('show');
});

