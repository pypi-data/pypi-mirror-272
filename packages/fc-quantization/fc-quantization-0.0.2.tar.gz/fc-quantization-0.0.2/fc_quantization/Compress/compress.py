from FeatureCloud.app.engine.app import AppState
from typing import TypedDict
from torch.utils.data import DataLoader
import torch
import utils
import io




class QuantType(TypedDict):
    model: torch.nn.Module
    train_loader: DataLoader
    epochs: int
    learning_rate: float
    backend: str
    quant_type: str


class QuantAppState(AppState):

    def configure_quant(self, model: torch.nn.Module = None, backend: str = 'qnnpack', quant_type: str = 'post_static'):

        '''
        Configures the quantization settings for your model.

        Parameters
        ----------
        model : torch.nn.Module, optional
            Your PyTorch model. Default is None.
        backend : str, optional
            Backend for quantization.
            Supports 'fbgemm' and 'qnnpack'.
            Default is 'qnnpack'.
        quant_type : str, optional
            Type of quantization. Supported is post-static quantization: 'post_static'
            and quantization-aware training: 'qat'.
            Default is 'post_static'.
        '''

        if self.load('default_quant') is None:
            self.store('default_quant', QuantType())

        default_quant = self.load('default_quant')

        updated_quant = default_quant.copy()

        updated_quant['model'] = model
        updated_quant['backend'] = backend
        updated_quant['quant_type'] = quant_type

        self.store('default_quant', updated_quant)




    def gather_data(self, use_quant=True, **kwargs):
        '''
                Gathers data for federated learning, including quantization if enabled.

                Parameters
                ----------
                use_quant : bool, optional
                    Flag to indicate whether to use quantization. Default is True.

                Returns
                -------
                data : list
                    List of data to be sent to the coordinator.
                '''

        data = super().gather_data(**kwargs)
        if use_quant:

            reference_model = self.load('reference_model')
            backend = self.load('backend')

            print(data)
            self.log(f'Size of model before rebuild: {utils.print_size_of_model(reference_model)} MB')

            reconstructed_models = []
            # reconstruct data after quantization
            for i in range(len(data)):
                print('Reconstrucing Models')

                # recreating client models by first quantizing reference model and loading quantized model after
                client_model = self.load('reference_model')
                client_model.eval()
                client_model.qconfig = torch.quantization.get_default_qat_qconfig(backend)
                client_model = torch.quantization.prepare(client_model, inplace=False)
                client_model = torch.quantization.convert(client_model, inplace=False)
                data[i].seek(0)
                client_model.load_state_dict(torch.load(data[i]))


                rebuild_model = utils.revert_quantized_model(client_model, reference_model)

                reconstructed_models.append(utils.get_weights(rebuild_model))

            data = reconstructed_models

        return data

    def send_data_to_coordinator(self, data, use_quant = True, **kwargs):
        '''
            Sends data to the coordinator, including quantization if enabled.

            Parameters
            ----------
            data : list
                List of data to be sent to the coordinator.
            use_quant : bool, optional
                Flag to indicate whether to use quantization. Default is True.

            Returns
            -------
            data : list
                List of data sent to the coordinator.
            '''
        if use_quant:
            default_quant = self.load('default_quant')
            quant_type = default_quant['quant_type']
            model = data
            backend = default_quant['backend']

            self.store('default_quant', default_quant)

            self.log('Start Quantization...')
            self.log(f'Size of model before quantization: {utils.print_size_of_model(model)} MB')

            if quant_type == 'post_static':
                self.log('Apply Post-Static-Quantization...')
                model = torch.quantization.convert(model, inplace=False)

            elif quant_type == 'qat':
                self.log('Apply QAT-Quantization...')
                model = torch.quantization.convert(model, inplace=False)


            else:
                raise ValueError('quant_type must be either post_static or qat')

            self.log(f'Size of model after quantization: {utils.print_size_of_model(model)} MB')

            b = io.BytesIO()
            torch.save(model.state_dict(), b)
            data = b
            super().send_data_to_coordinator(data, **kwargs)
        else:
            super().send_data_to_coordinator(data, **kwargs)
        return data