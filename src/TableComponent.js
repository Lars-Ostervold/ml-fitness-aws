import React, { useState } from 'react';

const TableComponent = ({ exerciseData }) => {

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Column 1</th>
            <th>Column 2</th>
            <th>Column 3</th>
            {/* Add more column headings as needed */}
          </tr>
        </thead>
        <tbody>
          {exerciseData.map((row, index) => (
            <tr key={index}>
              <td>{row[0]}</td>
              <td>{row[1]}</td>
              <td>{row[2]}</td>
              {/* Render more columns based on the row array */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
