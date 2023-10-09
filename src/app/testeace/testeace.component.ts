import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-testeace',
  templateUrl: './testeace.component.html',
  styleUrls: ['./testeace.component.css']
})
export class TesteaceComponent implements OnInit {
  panelOpenState = false;
  showFiller = false;
  regras = [
    { nome: "[1] Regra consulta apontamento", disparos: 347, habilitado: true },
    { nome: "[2] Regra consulta apontamento", disparos: 346, habilitado: true },
    { nome: "[3] Regra consulta apontamento", disparos: 376, habilitado: true },
    { nome: "[4] Regra consulta apontamento", disparos: 476, habilitado: true },
    { nome: "[5] Regra consulta apontamento", disparos: 34, habilitado: true },
    { nome: "[6] Regra consulta apontamento", disparos: 76, habilitado: true },
    { nome: "[7] Regra consulta apontamento", disparos: 5476, habilitado: false },
    { nome: "[8] Regra consulta apontamento", disparos: 576, habilitado: true },
    { nome: "[9] Regra consulta apontamento", disparos: 3776, habilitado: true }]
  constructor() { }
  form: FormGroup = new FormGroup({
    tel: new FormControl('procurar regra'),
  });
  ngOnInit(): void {
  }

}
