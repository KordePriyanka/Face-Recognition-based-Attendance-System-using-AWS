document.addEventListener('DOMContentLoaded', () => {
	fetch('https://zcbhe1ripd.execute-api.ap-south-1.amazonaws.com/fetchstage/FetchFunction')
	  .then(response => response.json())
	  .then(data => {
		const tableBody = document.querySelector('#attendanceTable tbody');
		data.forEach(student => {
		  const row = document.createElement('tr');
		  const rollNoCell = document.createElement('td');
		  const nameCell = document.createElement('td');
		  const attendanceCell = document.createElement('td');

// Change Cridential like Name, Rollno and Count here....
		  rollNoCell.textContent = student.Rollno;
		  nameCell.textContent = student.Name;
		  attendanceCell.textContent = student.Count;
  
		  row.appendChild(rollNoCell);
		  row.appendChild(nameCell);
		  row.appendChild(attendanceCell);
		  tableBody.appendChild(row);
		});
	  })
	  .catch(error => {
		console.error('Error:', error);
	  });
  });
  
