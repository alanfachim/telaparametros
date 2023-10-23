import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { FloatLabelType } from '@angular/material/form-field';
import { PedidosService } from '../shared/sevice/pedidosService';

@Component({
  selector: 'app-testeace',
  templateUrl: './testeace.component.html',
  styleUrls: ['./testeace.component.css']
})
export class TesteaceComponent implements OnInit {
  panelOpenState = false;
  showFiller = false;
  hideRequiredControl = new FormControl(false);
  floatLabelControl = new FormControl('auto' as FloatLabelType);
  options = this._formBuilder.group({
    hideRequired: this.hideRequiredControl,
    floatLabel: this.floatLabelControl,
  });


  getFloatLabelValue(): FloatLabelType {
    return this.floatLabelControl.value || 'auto';
  }
  getpedidos(){
    this.pedidosService.listPedidos()
  }
  regras = [
    { nome: "[1] Regra consulta apontamento", disparos: 347, habilitado: true },
    { nome: "[2] Regra consulta apontamento", disparos: 346, habilitado: true },]
  constructor(private _formBuilder: FormBuilder, public pedidosService:PedidosService) { }
  form: FormGroup = new FormGroup({
    tel: new FormControl('procurar regra'),
  });
  ngOnInit(): void {
  }

}
