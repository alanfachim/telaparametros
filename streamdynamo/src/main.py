import threading
from fastapi import FastAPI
from input.encaminhamento_controller import EncaminhamentoController
from input.regra_controller import RegraController
from input.sqs import SQSPoller


app = FastAPI() 

regraController = RegraController()
regras = regraController.listar_regras()
sqs = SQSPoller('encaminha_requisicao_pedido.fifo')
encaminhamentoController = EncaminhamentoController(regras, sqs)

app.include_router(encaminhamentoController.router)
app.include_router(regraController.router)

def do_something():
    regras = regraController.listar_regras()
    regraController.regras = regras
    
# Criar um objeto Timer com o intervalo de 10 minutos e a função do_something
timer = threading.Timer(60, do_something)

# Iniciar a thread
timer.start()
 
class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            message = sqs.poll()
            if message:
                print(f'Mensagem enviada: {message}')
            else:
                print('Nenhuma mensagem recebida') 
                
if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
 