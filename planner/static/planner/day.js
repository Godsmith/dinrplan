$(document).ready(function () {
  let selectizeControl = $('#myselect');
  console.log(selectizeControl)
  var $select = selectizeControl.selectize({
    //    valueField: 'name',
    //    labelField: 'name',
    //    searchField: 'name',
    persist: false,
    delimiter: ';',
    //    openOnFocus: false,
    //    create: (input => {return {name: input}}),
    create: true,
    createOnBlur: true,
    onDropdownOpen: function() {
      // Manually prevent dropdown from opening when there is no search term
      if (!this.lastQuery.length) {
        this.close();
      }
    },
    onItemAdd: function() {
      // Close dropdown when choosing a meal
      this.close();
    }
  });

  // Store the reference to the selectize in the data property to be able to access it elsewhere
  // From here: http://stackoverflow.com/questions/24666297/how-to-get-the-value-of-the-currently-selected-selectize-js-input-item
  //selectizeControl.data('selectize', $select);

  // Only options in the list may be displayed in the box, so in order to be able to show
  // also meals that are not in the database in the input box we need to add them as options.
  //  var selectize = $select[0].selectize;
  //  mealsArray.forEach((mealName) => {
  //    selectize.addOption({name: mealName});
  //  });
  //  selectize.setValue(mealsArray);

  // Focus the input box here as well, or it will not be focused the first time after the user
  // has navigated to the page that they click an edit box
  //$("#select").focus();
});
