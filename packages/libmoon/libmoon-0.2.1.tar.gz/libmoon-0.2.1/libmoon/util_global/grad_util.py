
import torch


def get_moo_grad(x, y, n_obj):
    grad_arr = [0] * n_obj
    for obj_idx in range(n_obj):
        y[obj_idx].backward(retain_graph=True)
        grad_arr[obj_idx] = x.grad.clone()
        x.grad.zero_()

    grad_arr = torch.stack(grad_arr)
    return grad_arr


def get_moo_Jacobian(x, y, n_obj):
    grad_arr = [0] * n_obj
    for obj_idx in range(n_obj):
        y[obj_idx].backward(retain_graph=True)
        grad_arr[obj_idx] = x.grad.clone()
        x.grad.zero_()

    grad_arr = torch.stack(grad_arr)
    return grad_arr




def flatten_grads(grads_dict):
    return torch.cat( [v.view(-1) for _, v in grads_dict.items()] )




def calc_gradients(batch, model, objectives):
    # store gradients and objective values
    gradients = []
    obj_values = []
    for i, objective in enumerate(objectives):
        # zero grad
        model.zero_grad()

        logits = model(batch)
        batch.update(logits)

        output = objective(**batch)
        output.backward()

        obj_values.append(output.item())
        gradients.append({})

        private_params = model.private_params() if hasattr(model, 'private_params') else []
        for name, param in model.named_parameters():
            not_private = all([p not in name for p in private_params])
            if not_private and param.requires_grad and param.grad is not None:
                gradients[i][name] = param.grad.data.detach().clone()

    return gradients, obj_values


