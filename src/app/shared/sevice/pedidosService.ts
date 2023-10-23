import {
  HttpClient,
  HttpHeaders
} from '@angular/common/http';
import {
  Injectable
} from '@angular/core';
import {
  BehaviorSubject,
  firstValueFrom
} from 'rxjs';
import {
  environment
} from 'src/environments/environment';
import { presente } from './presentesService';

// Alterando a interface Pedido para se adequar ao modelo do objeto PedidoCredito
export interface Pedido {
  codigo_pedido_credito: any // Adicionando o atributo codigo_pedido_credito
  cnpj: any // Alterando o tipo de nome para cnpj
  status_pedido: any // Adicionando o atributo status_pedido
  segmento_bancario: any // Adicionando o atributo segmento_bancario
  codigo_canal_solicitacao: any // Adicionando o atributo codigo_canal_solicitacao
  descricao_canal_solicitacao: any // Adicionando o atributo descricao_canal_solicitacao
  valor_pedido: any // Alterando o tipo de email para valor_pedido
  unidade_monetaria: any // Adicionando o atributo unidade_monetaria
  nome_grupo: any // Alterando o tipo de texto para nome_grupo
  data_pedido: any // Alterando o tipo de meioPagamento para data_pedido
  prazo: any // Adicionando o atributo prazo
  unidade_prazo: any // Adicionando o atributo unidade_prazo
  codigo_identificacao_origem: any // Adicionando o atributo codigo_identificacao_origem
  parecer_origem_pedido: any // Adicionando o atributo parecer_origem_pedido
}

@Injectable({
  providedIn: 'root'
})
export class PedidosService {

  private _item: any;
  setCurrentOrder(item: any) {
    this._item = item;
  }
  getCurrentOrder() {
    return this._item;
  }
  private _pedidos: Pedido | undefined;
  private _listPedidos: Pedido[] | undefined;
  public listPedidosObj = new BehaviorSubject<any>(null);
  public PedidosObj = new BehaviorSubject<any>(null);

  private base_url = environment.base_url; // Alterando a base_url para apontar para o serviço de pedido de credito
  private subscription = environment.subscription;


  constructor(private http: HttpClient) { }


  putPedidos(pedido: Pedido, id: any): any {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': this.subscription
      })
    };
    return firstValueFrom(this.http.put<any>(`${this.base_url}/pedidos/${id}`, pedido, httpOptions)).then((response: any) => { // Alterando o método de post para put e usando o código do pedido como id
      this._pedidos = response;
      this.PedidosObj.next(this._pedidos);
    }).catch(erro => {
      console.log(erro);
    });
  }


  postPedidos(pedido: Pedido, id: any): void {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': this.subscription
      })
    };
    firstValueFrom(this.http.post<any>(`${this.base_url}/pedidos`, pedido, httpOptions)).then((response: any) => { // Removendo o parâmetro id que não é usado na rota post do serviço de pedido de credito
      this._pedidos = response;
      this.PedidosObj.next(this._pedidos);
    }).catch(erro => {
      console.log(erro);
    });
  }


  getPedidos(id: any): any {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': this.subscription
      })
    };
    return firstValueFrom(this.http.get<any>(`${this.base_url}/pedidos/${id}`, httpOptions)).then((response: any) => {
      this._pedidos = response; // Removendo o índice [0] que não é necessário na resposta do serviço de pedido de credito
      this.PedidosObj.next(this._pedidos);
      return this._pedidos;
    }).catch(erro => {
      console.log(erro);
    });
  }


  listPedidos(): void {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    firstValueFrom(this.http.get<any>(`${this.base_url}/pedidos`, httpOptions)).then((response: any) => {
      this._listPedidos = response;
      this.listPedidosObj.next(this._listPedidos);
    }).catch(erro => {
      console.log(erro);
    });
  }
  // Alterando o método de listar pedidos para receber os parâmetros da query string
  listPedidos2(segmento_bancario: any, cnpj: any): void { // Adicionando os parâmetros segmento_bancario e cnpj
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    // Adicionando os parâmetros à url da requisição
    firstValueFrom(this.http.get<any>(`${this.base_url}/pedidos?segmento_bancario=${segmento_bancario}&cnpj=${cnpj}`, httpOptions)).then((response: any) => {
      this._listPedidos = response;
      this.listPedidosObj.next(this._listPedidos);
    }).catch(erro => {
      console.log(erro);
    });
  }

  // Adicionando um método para deletar um pedido pelo código
  deletePedidos(id: any): any {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': this.subscription
      })
    };
    return firstValueFrom(this.http.delete<any>(`${this.base_url}/pedidos/${id}`, httpOptions)).then((response: any) => {
      this._pedidos = response; // Recebendo a resposta do serviço de pedido de credito
      this.PedidosObj.next(this._pedidos);
      return this._pedidos;
    }).catch(erro => {
      console.log(erro);
    });
  }
}
