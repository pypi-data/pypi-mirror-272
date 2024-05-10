# tse-rating
```rate-artifact sub-003_ses_01_acq_hipp_T2w.nii.gz```

```ruby
from artifact_rating import rate_motion_artifact
input_path = 'sub-003_ses-01_acq-hipp_T2w.nii.gz'
score = rate_motion_artifact(input_path)
```
