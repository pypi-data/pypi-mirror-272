# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['S3BucketArgs', 'S3Bucket']

@pulumi.input_type
class S3BucketArgs:
    def __init__(__self__, *,
                 acl: Optional[pulumi.Input[str]] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 bucket_prefix: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 object_locking: Optional[pulumi.Input[bool]] = None,
                 quota: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a S3Bucket resource.
        """
        if acl is not None:
            pulumi.set(__self__, "acl", acl)
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        if force_destroy is not None:
            pulumi.set(__self__, "force_destroy", force_destroy)
        if object_locking is not None:
            pulumi.set(__self__, "object_locking", object_locking)
        if quota is not None:
            pulumi.set(__self__, "quota", quota)

    @property
    @pulumi.getter
    def acl(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "acl")

    @acl.setter
    def acl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl", value)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_prefix")

    @bucket_prefix.setter
    def bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_prefix", value)

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "force_destroy")

    @force_destroy.setter
    def force_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_destroy", value)

    @property
    @pulumi.getter(name="objectLocking")
    def object_locking(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "object_locking")

    @object_locking.setter
    def object_locking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "object_locking", value)

    @property
    @pulumi.getter
    def quota(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "quota")

    @quota.setter
    def quota(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "quota", value)


@pulumi.input_type
class _S3BucketState:
    def __init__(__self__, *,
                 acl: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 bucket_domain_name: Optional[pulumi.Input[str]] = None,
                 bucket_prefix: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 object_locking: Optional[pulumi.Input[bool]] = None,
                 quota: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering S3Bucket resources.
        """
        if acl is not None:
            pulumi.set(__self__, "acl", acl)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if bucket_domain_name is not None:
            pulumi.set(__self__, "bucket_domain_name", bucket_domain_name)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        if force_destroy is not None:
            pulumi.set(__self__, "force_destroy", force_destroy)
        if object_locking is not None:
            pulumi.set(__self__, "object_locking", object_locking)
        if quota is not None:
            pulumi.set(__self__, "quota", quota)

    @property
    @pulumi.getter
    def acl(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "acl")

    @acl.setter
    def acl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="bucketDomainName")
    def bucket_domain_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_domain_name")

    @bucket_domain_name.setter
    def bucket_domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_domain_name", value)

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_prefix")

    @bucket_prefix.setter
    def bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_prefix", value)

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "force_destroy")

    @force_destroy.setter
    def force_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_destroy", value)

    @property
    @pulumi.getter(name="objectLocking")
    def object_locking(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "object_locking")

    @object_locking.setter
    def object_locking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "object_locking", value)

    @property
    @pulumi.getter
    def quota(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "quota")

    @quota.setter
    def quota(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "quota", value)


class S3Bucket(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl: Optional[pulumi.Input[str]] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 bucket_prefix: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 object_locking: Optional[pulumi.Input[bool]] = None,
                 quota: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_minio as minio

        state_terraform_s3 = minio.S3Bucket("state_terraform_s3",
            bucket="state-terraform-s3",
            acl="public")
        pulumi.export("minioId", state_terraform_s3.id)
        pulumi.export("minioUrl", state_terraform_s3.bucket_domain_name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[S3BucketArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_minio as minio

        state_terraform_s3 = minio.S3Bucket("state_terraform_s3",
            bucket="state-terraform-s3",
            acl="public")
        pulumi.export("minioId", state_terraform_s3.id)
        pulumi.export("minioUrl", state_terraform_s3.bucket_domain_name)
        ```

        :param str resource_name: The name of the resource.
        :param S3BucketArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(S3BucketArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl: Optional[pulumi.Input[str]] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 bucket_prefix: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 object_locking: Optional[pulumi.Input[bool]] = None,
                 quota: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = S3BucketArgs.__new__(S3BucketArgs)

            __props__.__dict__["acl"] = acl
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["bucket_prefix"] = bucket_prefix
            __props__.__dict__["force_destroy"] = force_destroy
            __props__.__dict__["object_locking"] = object_locking
            __props__.__dict__["quota"] = quota
            __props__.__dict__["arn"] = None
            __props__.__dict__["bucket_domain_name"] = None
        super(S3Bucket, __self__).__init__(
            'minio:index/s3Bucket:S3Bucket',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acl: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            bucket_domain_name: Optional[pulumi.Input[str]] = None,
            bucket_prefix: Optional[pulumi.Input[str]] = None,
            force_destroy: Optional[pulumi.Input[bool]] = None,
            object_locking: Optional[pulumi.Input[bool]] = None,
            quota: Optional[pulumi.Input[int]] = None) -> 'S3Bucket':
        """
        Get an existing S3Bucket resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _S3BucketState.__new__(_S3BucketState)

        __props__.__dict__["acl"] = acl
        __props__.__dict__["arn"] = arn
        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["bucket_domain_name"] = bucket_domain_name
        __props__.__dict__["bucket_prefix"] = bucket_prefix
        __props__.__dict__["force_destroy"] = force_destroy
        __props__.__dict__["object_locking"] = object_locking
        __props__.__dict__["quota"] = quota
        return S3Bucket(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def acl(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "acl")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="bucketDomainName")
    def bucket_domain_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bucket_domain_name")

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "bucket_prefix")

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "force_destroy")

    @property
    @pulumi.getter(name="objectLocking")
    def object_locking(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "object_locking")

    @property
    @pulumi.getter
    def quota(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "quota")

