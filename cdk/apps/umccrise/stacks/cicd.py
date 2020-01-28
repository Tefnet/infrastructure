from aws_cdk import (
    core,
    aws_codebuild as cb,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_s3 as s3,
)

class CICDStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # As semver dictates: https://regex101.com/r/Ly7O1x/3/
        semver_tag_regex = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        refdata = s3.Bucket.from_bucket_attributes(
            self, 'reference_data',
            bucket_name='umccr-refdata-dev'
        )

        build_env = cb.BuildEnvironment(build_image=cb.LinuxBuildImage.from_docker_registry("docker:dind"),
                                        privileged=True,
                                        compute_type=cb.ComputeType.MEDIUM);

        ecr_repo = ecr.Repository(self, id="umccr", repository_name="umccr");

        cb_project = cb.Project(self, id = "umccrise",
                    environment = build_env,
                    timeout = core.Duration.hours(3),
                    source = cb.Source.git_hub(
                        identifier = "umccrise",
                        owner = "umccr",
                        repo = "umccrise",
                        clone_depth = 1,
                        webhook = True,
                        webhook_filters=[ cb.FilterGroup.in_event_of(cb.EventAction.PUSH).and_tag_is(semver_tag_regex) ]
                    )
        );

        # Tackle IAM permissions
        # https://stackoverflow.com/questions/38587325/aws-ecr-getauthorizationtoken/54806087
        cb_project.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryPowerUser'));
        refdata.grant_read(cb_project);

app = core.App();
CICDStack(app, "UmccriseCICDStack");

app.synth()