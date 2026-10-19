def main():
    try:
        import torch
    except ImportError as exc:
        raise SystemExit("PyTorch is not installed. Install it from https://pytorch.org/get-started/locally/") from exc

    print("PyTorch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("CUDA runtime:", torch.version.cuda)
        print("GPU:", torch.cuda.get_device_name(0))
        print("Device count:", torch.cuda.device_count())
    else:
        print("PPO with an MLP often benefits more from CPU rollout throughput than GPU acceleration.")
        print("For neural vision models, a working CUDA-enabled PyTorch build is useful.")


if __name__ == "__main__":
    main()
