const modelos = [
  { codigo: 'M0123', marca: 'FORD', ano: 2025, modelo: 'FORD TERRITORY SEL' },
  { codigo: 'M0124', marca: 'PORSHE', ano: 2020, modelo: 'MACAN GTS' },
  { codigo: 'M0125', marca: 'TOYOTA', ano: 2023, modelo: 'COROLLA GLI 2.0 FLEX' },
  { codigo: 'M0126', marca: 'TOYOTA', ano: 2023, modelo: 'COROLLA GLI 2.0 FLEX' },
  { codigo: 'M0127', marca: 'VOLKSWAGEN', ano: 2022, modelo: 'POLO COMFORTLINE 1.0 TSI' },
  { codigo: 'M0128', marca: 'AUDI', ano: 2020, modelo: 'AUDI A3 S-LINE LIMITED 2.4' },
  { codigo: 'M0129', marca: 'BMW', ano: 2024, modelo: 'BMW X1' },
  { codigo: 'M0130', marca: 'MERCEDES', ano: 2024, modelo: 'C 200 AMG LINE' },
];

function carregarTabela() {
  const tabela = document.getElementById('modelTable');
  tabela.innerHTML = '';

  modelos.forEach((item) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.codigo}</td>
      <td>${item.marca}</td>
      <td>${item.ano}</td>
      <td>${item.modelo}</td>
      <td class="actions">
       <button class="edit"><i class="fas fa-edit"></i></button>
       <button class="delete"><i class="fas fa-trash-alt"></i></button>
      </td>
    `;
    tabela.appendChild(row);

    // Função editar
    row.querySelector('.edit').addEventListener('click', () => {
      alert('Editar modelo: ' + item.codigo);
    });

    // Função deletar
    row.querySelector('.delete').addEventListener('click', () => {
      const confirmacao = confirm('Tem certeza que deseja excluir o modelo: ' + item.codigo + '?');
      if (confirmacao) {
        alert('Modelo ' + item.codigo + ' excluído com sucesso!');
      }
    });
  });
}

document.getElementById('addModel').addEventListener('click', () => {
  alert('Função de adicionar modelo ainda não implementada.');
});

document.addEventListener('DOMContentLoaded', carregarTabela);
