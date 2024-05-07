# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['S3ObjectArgs', 'S3Object']

@pulumi.input_type
class S3ObjectArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str],
                 object_name: pulumi.Input[str],
                 content: Optional[pulumi.Input[str]] = None,
                 content_base64: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a S3Object resource.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "object_name", object_name)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_base64 is not None:
            pulumi.set(__self__, "content_base64", content_base64)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if source is not None:
            pulumi.set(__self__, "source", source)
        if version_id is not None:
            pulumi.set(__self__, "version_id", version_id)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="objectName")
    def object_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "object_name")

    @object_name.setter
    def object_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "object_name", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentBase64")
    def content_base64(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_base64")

    @content_base64.setter
    def content_base64(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_base64", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def source(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "version_id")

    @version_id.setter
    def version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_id", value)


@pulumi.input_type
class _S3ObjectState:
    def __init__(__self__, *,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_base64: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 object_name: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering S3Object resources.
        """
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_base64 is not None:
            pulumi.set(__self__, "content_base64", content_base64)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if object_name is not None:
            pulumi.set(__self__, "object_name", object_name)
        if source is not None:
            pulumi.set(__self__, "source", source)
        if version_id is not None:
            pulumi.set(__self__, "version_id", version_id)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentBase64")
    def content_base64(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_base64")

    @content_base64.setter
    def content_base64(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_base64", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="objectName")
    def object_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "object_name")

    @object_name.setter
    def object_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "object_name", value)

    @property
    @pulumi.getter
    def source(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "version_id")

    @version_id.setter
    def version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_id", value)


class S3Object(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_base64: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 object_name: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_minio as minio

        state_terraform_s3 = minio.S3Bucket("state_terraform_s3",
            bucket="state-terraform-s3",
            acl="public")
        txt_file = minio.S3Object("txt_file",
            bucket_name=state_terraform_s3.bucket,
            object_name="text.txt",
            content="Lorem ipsum dolor sit amet.",
            content_type="text/plain",
            opts=pulumi.ResourceOptions(depends_on=[state_terraform_s3]))
        pulumi.export("minioId", txt_file.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: S3ObjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_minio as minio

        state_terraform_s3 = minio.S3Bucket("state_terraform_s3",
            bucket="state-terraform-s3",
            acl="public")
        txt_file = minio.S3Object("txt_file",
            bucket_name=state_terraform_s3.bucket,
            object_name="text.txt",
            content="Lorem ipsum dolor sit amet.",
            content_type="text/plain",
            opts=pulumi.ResourceOptions(depends_on=[state_terraform_s3]))
        pulumi.export("minioId", txt_file.id)
        ```

        :param str resource_name: The name of the resource.
        :param S3ObjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(S3ObjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_base64: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 object_name: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = S3ObjectArgs.__new__(S3ObjectArgs)

            if bucket_name is None and not opts.urn:
                raise TypeError("Missing required property 'bucket_name'")
            __props__.__dict__["bucket_name"] = bucket_name
            __props__.__dict__["content"] = content
            __props__.__dict__["content_base64"] = content_base64
            __props__.__dict__["content_type"] = content_type
            __props__.__dict__["etag"] = etag
            if object_name is None and not opts.urn:
                raise TypeError("Missing required property 'object_name'")
            __props__.__dict__["object_name"] = object_name
            __props__.__dict__["source"] = source
            __props__.__dict__["version_id"] = version_id
        super(S3Object, __self__).__init__(
            'minio:index/s3Object:S3Object',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket_name: Optional[pulumi.Input[str]] = None,
            content: Optional[pulumi.Input[str]] = None,
            content_base64: Optional[pulumi.Input[str]] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            object_name: Optional[pulumi.Input[str]] = None,
            source: Optional[pulumi.Input[str]] = None,
            version_id: Optional[pulumi.Input[str]] = None) -> 'S3Object':
        """
        Get an existing S3Object resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _S3ObjectState.__new__(_S3ObjectState)

        __props__.__dict__["bucket_name"] = bucket_name
        __props__.__dict__["content"] = content
        __props__.__dict__["content_base64"] = content_base64
        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["etag"] = etag
        __props__.__dict__["object_name"] = object_name
        __props__.__dict__["source"] = source
        __props__.__dict__["version_id"] = version_id
        return S3Object(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="contentBase64")
    def content_base64(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "content_base64")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="objectName")
    def object_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "object_name")

    @property
    @pulumi.getter
    def source(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "version_id")

