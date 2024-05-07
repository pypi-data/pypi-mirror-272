import sys
sys.path.append("..")

import torch, argparse
from torch.nn import MSELoss
from pssr.models import ResUNet, ResUNetA, RDResUNet, RDResUNetA, SwinIR
from pssr.data import ImageDataset, SlidingDataset, PairedImageDataset, PairedSlidingDataset
from pssr.crappifiers import MultiCrappifier, Poisson, AdditiveGaussian, SaltPepper
from pssr.loss import SSIMLoss
from pssr.train import train_paired
from pssr.predict import predict_images, test_metrics

def _handle_declaration(arg, defaults, req=None):
    req = ", ".join(req)+", " if req is not None else ""

    if arg in defaults:
        expression = arg+f"({req})"
    else:
        expression = arg.split("(")[0]+f"({req}"+arg.split("(")[1]

    return eval(expression)

def parse():
    parser = argparse.ArgumentParser(prog="pssr", description="PSSR CLI for basic usage", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-t", "--train", action="store_true", help="enable train mode")

    parser.add_argument("-dp", "--data-path", type=str, help="specify dataset path")
    parser.add_argument("-dt", "--data-type", type=str, default="ImageDataset", help="specify dataset type")
    parser.add_argument("-mt", "--model-type", type=str, default="ResUNet", help="specify model type")
    parser.add_argument("-mp", "--model-path", type=str, help="specify model path")

    parser.add_argument("-e", "--epochs", type=int, default=10, help="specify number of training epochs")
    parser.add_argument("-b", "--batch-size", type=int, default=16, help="specify batch size")
    parser.add_argument("-lr", "--lr", type=float, default=1e-3, help="specify learning rate")
    parser.add_argument("-p", "--patience", type=int, default=3, help="specify learning rate decay patience")
    parser.add_argument("-mse", "--mse", action="store_true", help="use MSE loss instead of SSIM loss")

    parser.add_argument("-cp", "--checkpoint", action="store_true", help="save model checkpoints during training")
    parser.add_argument("-sl", "--save-losses", action="store_true", help="save training losses")

    return parser

def main():
    parser = parse()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return
    args = parser.parse_args()

    if "Paired" not in args.data_type and args.data_path is None:
        print("--data-path(-dp) must be provided for semi-synthetic datasets")
        return
    
    if args.model_path is None and not args.train:
        print("--model-path(-mp) must be provided in predict mode")
        return

    model = _handle_declaration(args.model_type, ["ResUNet", "ResUNetA", "RDResUNet", "RDResUNetA", "SwinIR"])
    dataset = _handle_declaration(args.data_type, ["ImageDataset", "SlidingDataset"], 
        req=[f"'{args.data_path}'"] if args.train else [f'''{f"'{args.data_path}', " if "Paired" not in args.data_type else ""}val_split=1'''])
    
    print(f"\nModel:\n{_tab_string(model.extra_repr())}")
    print(f"\nDataset:\n{_tab_string(str(dataset))}")

    if torch.cuda.is_available():
        device = "cuda"
        print("\nCUDA enabled device detected, running on GPU.")
    else:
        device = "cpu"
        print("\nCUDA enabled device NOT detected, running on CPU.")

    kwargs = dict(
        num_workers = 4,
        pin_memory = True,
    )

    if args.train:
        loss_fn = MSELoss() if args.mse else SSIMLoss(mix=.8, ms=True)
        optim = torch.optim.AdamW(model.parameters(), lr=args.lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optim, factor=0.1, patience=args.patience, threshold=5e-3, verbose=True)
        checkpoint_dir = "checkpoints" if args.checkpoint else None

        if args.model_path:
            print(f"Loading {model.__class__.__name__} model from {args.model_path}")
            model.load_state_dict(torch.load(args.model_path))

        print("\nTraining model...")
        train_losses, val_losses = train_paired(
            model=model,
            dataset=dataset,
            batch_size=args.batch_size,
            loss_fn=loss_fn,
            optim=optim,
            epochs=args.epochs,
            device=device,
            scheduler=scheduler,
            log_frequency=50,
            checkpoint_dir=checkpoint_dir,
            dataloader_kwargs=kwargs,
        )
        print("\nTraining complete!")

        save_path = f"{model.__class__.__name__}_{val_losses[-1]:.4f}.pth"
        torch.save(model.state_dict(), save_path)
        print(f"Saved trained model to {save_path}")

        if args.save_losses:
            with open(f"{model.__class__.__name__}_train_losses.txt", "w") as file:
                for loss in train_losses:
                    file.write(f"{loss:.6f}\n")
            with open(f"{model.__class__.__name__}_val_losses.txt", "w") as file:
                for loss in val_losses:
                    file.write(f"{loss:.6f}\n")

    else:
        model.load_state_dict(torch.load(args.model_path))

        print("\nPredicting images from low resolution...")
        predict_images(model, dataset, device, norm=not dataset.is_lr, out_dir="preds")

        if not dataset.is_lr:
            print("\nCalculating metrics...")
            metrics = test_metrics(model, dataset, device)

            print("\nMetrics:")
            for metric in metrics:
                print(f"{metric}: {metrics[metric]}")
    
    print("\n")

def _tab_string(text):
    lines = text.split("\n")
    indented_lines = ["\t" + line for line in lines]
    return "\n".join(indented_lines)

if __name__ == "__main__":
    main()
