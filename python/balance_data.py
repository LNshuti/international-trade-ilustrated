from balance import load_data, Sample

def main():
    # load simulated example data
    target_df, sample_df = load_data()

    # Import sample and target data into a Sample object
    sample = Sample.from_frame(sample_df, outcome_columns=["happiness"])
    target = Sample.from_frame(target_df)

    # Set the target to be the target of sample
    sample_with_target = sample.set_target(target)

    # Check basic diagnostics of sample vs target before adjusting:
    sample_with_target.covars().plot()

if __name__ == '__main__':
    main()