from __future__ import annotations
import typing

import typing_extensions

#class File(typing_extensions.TypedDict, total=False): _parent: str #ADDED

_list = list


class About(typing_extensions.TypedDict, total=False):
    appInstalled: bool
    canCreateDrives: bool
    canCreateTeamDrives: bool
    driveThemes: _list[dict[str, typing.Any]]
    exportFormats: dict[str, typing.Any]
    folderColorPalette: _list[str]
    importFormats: dict[str, typing.Any]
    kind: str
    maxImportSizes: dict[str, typing.Any]
    maxUploadSize: str
    storageQuota: dict[str, typing.Any]
    teamDriveThemes: _list[dict[str, typing.Any]]
    user: User


class Change(typing_extensions.TypedDict, total=False):
    changeType: str
    drive: Drive
    driveId: str
    file: File
    fileId: str
    kind: str
    removed: bool
    teamDrive: TeamDrive
    teamDriveId: str
    time: str
    type: str


class ChangeList(typing_extensions.TypedDict, total=False):
    changes: _list[Change]
    kind: str
    newStartPageToken: str
    nextPageToken: str


class Channel(typing_extensions.TypedDict, total=False):
    address: str
    expiration: str
    id: str
    kind: str
    params: dict[str, typing.Any]
    payload: bool
    resourceId: str
    resourceUri: str
    token: str
    type: str


class Comment(typing_extensions.TypedDict, total=False):
    anchor: str
    author: User
    content: str
    createdTime: str
    deleted: bool
    htmlContent: str
    id: str
    kind: str
    modifiedTime: str
    quotedFileContent: dict[str, typing.Any]
    replies: _list[Reply]
    resolved: bool


class CommentList(typing_extensions.TypedDict, total=False):
    comments: _list[Comment]
    kind: str
    nextPageToken: str


class ContentRestriction(typing_extensions.TypedDict, total=False):
    readOnly: bool
    reason: str
    restrictingUser: User
    restrictionTime: str
    type: str


class Drive(typing_extensions.TypedDict, total=False):
    backgroundImageFile: dict[str, typing.Any]
    backgroundImageLink: str
    capabilities: dict[str, typing.Any]
    colorRgb: str
    createdTime: str
    hidden: bool
    id: str
    kind: str
    name: str
    orgUnitId: str
    restrictions: dict[str, typing.Any]
    themeId: str


class DriveList(typing_extensions.TypedDict, total=False):
    drives: _list[Drive]
    kind: str
    nextPageToken: str


class FileBase(typing_extensions.TypedDict, total=False):
    createdTime: str
    id: str
    md5Checksum: str
    mimeType: str
    modifiedTime: str
    name: str
    parents: _list[str]
    sha1Checksum: str
    sha256Checksum: str
    size: str
    trashed: bool

class File(FileBase, total=False):
    appProperties: dict[str, typing.Any]
    capabilities: dict[str, typing.Any]
    contentHints: dict[str, typing.Any]
    contentRestrictions: _list[ContentRestriction]
    copyRequiresWriterPermission: bool
    description: str
    driveId: str
    explicitlyTrashed: bool
    exportLinks: dict[str, typing.Any]
    fileExtension: str
    folderColorRgb: str
    fullFileExtension: str
    hasAugmentedPermissions: bool
    hasThumbnail: bool
    headRevisionId: str
    iconLink: str
    imageMediaMetadata: dict[str, typing.Any]
    isAppAuthorized: bool
    kind: str
    labelInfo: dict[str, typing.Any]
    lastModifyingUser: User
    linkShareMetadata: dict[str, typing.Any]
    modifiedByMe: bool
    modifiedByMeTime: str
    originalFilename: str
    ownedByMe: bool
    owners: _list[User]
    #_parent: str #ADDED
    permissionIds: _list[str]
    permissions: _list[Permission]
    properties: dict[str, typing.Any]
    quotaBytesUsed: str
    resourceKey: str
    shared: bool
    sharedWithMeTime: str
    sharingUser: User
    shortcutDetails: dict[str, typing.Any]
    spaces: _list[str]
    starred: bool
    teamDriveId: str
    thumbnailLink: str
    thumbnailVersion: str
    trashedTime: str
    trashingUser: User
    version: str
    videoMediaMetadata: dict[str, typing.Any]
    viewedByMe: bool
    viewedByMeTime: str
    viewersCanCopyContent: bool
    webContentLink: str
    webViewLink: str
    writersCanShare: bool


class FileList(typing_extensions.TypedDict, total=False):
    files: _list[File]
    incompleteSearch: bool
    kind: str
    nextPageToken: str


class GeneratedIds(typing_extensions.TypedDict, total=False):
    ids: _list[str]
    kind: str
    space: str


class Label(typing_extensions.TypedDict, total=False):
    fields: dict[str, typing.Any]
    id: str
    kind: str
    revisionId: str


class LabelField(typing_extensions.TypedDict, total=False):
    dateString: _list[str]
    id: str
    integer: _list[str]
    kind: str
    selection: _list[str]
    text: _list[str]
    user: _list[User]
    valueType: str


class LabelFieldModification(typing_extensions.TypedDict, total=False):
    fieldId: str
    kind: str
    setDateValues: _list[str]
    setIntegerValues: _list[str]
    setSelectionValues: _list[str]
    setTextValues: _list[str]
    setUserValues: _list[str]
    unsetValues: bool


class LabelList(typing_extensions.TypedDict, total=False):
    kind: str
    labels: _list[Label]
    nextPageToken: str


class LabelModification(typing_extensions.TypedDict, total=False):
    fieldModifications: _list[LabelFieldModification]
    kind: str
    labelId: str
    removeLabel: bool


class ModifyLabelsRequest(typing_extensions.TypedDict, total=False):
    kind: str
    labelModifications: _list[LabelModification]


class ModifyLabelsResponse(typing_extensions.TypedDict, total=False):
    kind: str
    modifiedLabels: _list[Label]


class Permission(typing_extensions.TypedDict, total=False):
    allowFileDiscovery: bool
    deleted: bool
    displayName: str
    domain: str
    emailAddress: str
    expirationTime: str
    id: str
    kind: str
    pendingOwner: bool
    permissionDetails: _list[dict[str, typing.Any]]
    photoLink: str
    role: str
    teamDrivePermissionDetails: _list[dict[str, typing.Any]]
    type: str
    view: str


class PermissionList(typing_extensions.TypedDict, total=False):
    kind: str
    nextPageToken: str
    permissions: _list[Permission]


class Reply(typing_extensions.TypedDict, total=False):
    action: str
    author: User
    content: str
    createdTime: str
    deleted: bool
    htmlContent: str
    id: str
    kind: str
    modifiedTime: str


class ReplyList(typing_extensions.TypedDict, total=False):
    kind: str
    nextPageToken: str
    replies: _list[Reply]


class Revision(typing_extensions.TypedDict, total=False):
    exportLinks: dict[str, typing.Any]
    id: str
    keepForever: bool
    kind: str
    lastModifyingUser: User
    md5Checksum: str
    mimeType: str
    modifiedTime: str
    originalFilename: str
    publishAuto: bool
    published: bool
    publishedLink: str
    publishedOutsideDomain: bool
    size: str


class RevisionList(typing_extensions.TypedDict, total=False):
    kind: str
    nextPageToken: str
    revisions: _list[Revision]


class StartPageToken(typing_extensions.TypedDict, total=False):
    kind: str
    startPageToken: str


class TeamDrive(typing_extensions.TypedDict, total=False):
    backgroundImageFile: dict[str, typing.Any]
    backgroundImageLink: str
    capabilities: dict[str, typing.Any]
    colorRgb: str
    createdTime: str
    id: str
    kind: str
    name: str
    orgUnitId: str
    restrictions: dict[str, typing.Any]
    themeId: str


class TeamDriveList(typing_extensions.TypedDict, total=False):
    kind: str
    nextPageToken: str
    teamDrives: _list[TeamDrive]


class User(typing_extensions.TypedDict, total=False):
    displayName: str
    emailAddress: str
    kind: str
    me: bool
    permissionId: str
    photoLink: str
